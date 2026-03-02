def enrich_city_data(df):
    # Congestion ratio
    df["congestion_ratio"] = df["current_speed_kmh"] / df["free_flow_speed_kmh"]
    df["congestion_ratio"] = df["congestion_ratio"].fillna(0)

    # Normalize AQI (simple scaling)
    df["aqi_normalized"] = df["aqi"] / df["aqi"].max()

    # Urban Stress Score (balanced weight)
    df["urban_stress_score"] = 0.5 * df["aqi_normalized"] + 0.5 * (
        1 - df["congestion_ratio"]
    )

    # Risk classification
    def classify(aqi):
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Satisfactory"
        elif aqi <= 200:
            return "Moderate"
        elif aqi <= 300:
            return "Poor"
        elif aqi <= 400:
            return "Very Poor"
        else:
            return "Severe"

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
