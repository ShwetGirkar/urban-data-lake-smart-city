from app.models.traffic_model import predict_peak_hours
from app.models.aqi_model import predict_aqi_alert
from app.models.urban_stress_model import calculate_urban_stress, rank_cities_by_stress
from app.models.city_alert_model import generate_city_alerts


def get_traffic_prediction(city: str):
    result = predict_peak_hours(city)
    return result


def get_aqi_prediction(city: str):
    result = predict_aqi_alert(city)
    return result


def get_city_stress(city: str):
    return calculate_urban_stress(city)


def get_stress_ranking():
    return rank_cities_by_stress()


def get_city_alerts():
    return generate_city_alerts()
