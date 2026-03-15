import pandas as pd


# US EPA AQI breakpoints
PM25_BREAKPOINTS = [
    (0.0, 12.0, 0, 50),
    (12.1, 35.4, 51, 100),
    (35.5, 55.4, 101, 150),
    (55.5, 150.4, 151, 200),
    (150.5, 250.4, 201, 300),
    (250.5, 350.4, 301, 400),
    (350.5, 500.4, 401, 500),
]

PM10_BREAKPOINTS = [
    (0, 54, 0, 50),
    (55, 154, 51, 100),
    (155, 254, 101, 150),
    (255, 354, 151, 200),
    (355, 424, 201, 300),
    (425, 504, 301, 400),
    (505, 604, 401, 500),
]


def calculate_aqi(concentration, breakpoints):
    for bp_lo, bp_hi, aqi_lo, aqi_hi in breakpoints:
        if bp_lo <= concentration <= bp_hi:
            return round(
                ((aqi_hi - aqi_lo) / (bp_hi - bp_lo)) * (concentration - bp_lo) + aqi_lo
            )
    return None


def compute_us_aqi(components):
    pm25 = components.get("pm2_5")
    pm10 = components.get("pm10")

    pm25_aqi = calculate_aqi(pm25, PM25_BREAKPOINTS) if pm25 else None
    pm10_aqi = calculate_aqi(pm10, PM10_BREAKPOINTS) if pm10 else None

    values = [v for v in [pm25_aqi, pm10_aqi] if v is not None]

    if not values:
        return None

    return max(values)


def enrich_city_data(df):

    # Calculate US AQI from PM values
    df["aqi"] = df.apply(
        lambda row: compute_us_aqi({"pm2_5": row["pm25"], "pm10": row["pm10"]}),
        axis=1,
    )

    # Congestion ratio
    df["congestion_ratio"] = 1 - (
        df["current_speed_kmh"] / df["free_flow_speed_kmh"].replace(0, pd.NA)
    )

    df["congestion_ratio"] = df["congestion_ratio"].clip(lower=0)
    df["congestion_ratio"] = df["congestion_ratio"].fillna(0)
    # Normalize AQI (0-500 scale)
    df["aqi_normalized"] = df["aqi"] / 500

    # Urban Stress Score
    df["urban_stress_score"] = 0.5 * df["aqi_normalized"] + 0.5 * (
        1 - df["congestion_ratio"]
    )

    # Risk classification (US AQI categories)
    def classify(aqi):
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Sensitive"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"

    df["risk_level"] = df["aqi"].apply(classify)

    return df


def compute_summary(df):
    df = enrich_city_data(df)

    avg_aqi = df["aqi"].mean()
    avg_temp = df["temperature_c"].mean()
    avg_congestion = df["congestion_ratio"].mean()

    worst_city_row = df.sort_values("urban_stress_score", ascending=False).iloc[0]
    worst_city = worst_city_row["city"]

    last_updated = df["timestamp_weather"].max()

    return {
        "avg_aqi": round(avg_aqi, 2),
        "avg_temperature": round(avg_temp, 2),
        "avg_congestion": round(avg_congestion, 2),
        "worst_city": worst_city,
        "last_updated": last_updated,
    }


def generate_alerts(df):

    df = enrich_city_data(df)
    alerts = []

    for _, row in df.iterrows():
        city = row["city"]
        timestamp = row["timestamp_weather"]
        aqi = row["aqi"]

        # AQI Alerts (US AQI scale)
        if aqi >= 300:
            alerts.append(
                {
                    "level": "Critical",
                    "type": "AQI",
                    "city": city,
                    "message": f"Hazardous Air Quality (AQI: {aqi})",
                    "time": timestamp,
                }
            )

        elif aqi >= 200:
            alerts.append(
                {
                    "level": "High",
                    "type": "AQI",
                    "city": city,
                    "message": f"Very Unhealthy Air Quality (AQI: {aqi})",
                    "time": timestamp,
                }
            )

        elif aqi >= 150:
            alerts.append(
                {
                    "level": "Medium",
                    "type": "AQI",
                    "city": city,
                    "message": f"Unhealthy Air Quality (AQI: {aqi})",
                    "time": timestamp,
                }
            )

        # Traffic Alerts
        ratio = row.get("congestion_ratio", 1)

        if ratio > 0.4:
            alerts.append(
                {
                    "level": "High",
                    "type": "Traffic",
                    "city": city,
                    "message": "Severe congestion detected",
                    "time": timestamp,
                }
            )

        elif ratio > 0.6:
            alerts.append(
                {
                    "level": "Medium",
                    "type": "Traffic",
                    "city": city,
                    "message": "Moderate congestion detected",
                    "time": timestamp,
                }
            )

        # Weather Alerts
        if row["wind_speed_mps"] > 10:
            alerts.append(
                {
                    "level": "High",
                    "type": "Weather",
                    "city": city,
                    "message": f"High wind speed ({row['wind_speed_mps']} m/s)",
                    "time": timestamp,
                }
            )

    return alerts
