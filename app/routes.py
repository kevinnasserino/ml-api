from flask import Blueprint, request, jsonify
from tsp import solve_tsp
from cbf import recommend
from datetime import datetime
import pandas as pd

main_blueprint = Blueprint("main", __name__)

def calculate_duration(start_date, end_date):
    start = datetime.strptime(start_date, "%d-%m-%Y")
    end = datetime.strptime(end_date, "%d-%m-%Y")
    return (end - start).days + 1

@main_blueprint.route('/recommend', methods=['POST'])
def recommend_itinerary():
    data = request.get_json()
    city = data.get("city")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    price_category = data.get("price_category")

    if not all([city, start_date, end_date, price_category]):
        return jsonify({"error": "Missing required fields"}), 400

    num_days = calculate_duration(start_date, end_date)
    recommendations_per_slot = {
        slot: recommend(city, price_category, slot, top_n=3)
        for slot in ['morning', 'afternoon', 'evening']
    }
    selected_places = []
    for day in range(num_days):
        day_places = {}
        for slot, rec in recommendations_per_slot.items():
            if not rec.empty:
                selected_place = rec.iloc[0]
                day_places[slot] = selected_place.to_dict()
                recommendations_per_slot[slot] = rec.iloc[1:]
        selected_places.append(day_places)

    optimized_routes = []
    for day_places in selected_places:
        places_with_coords = {
            place['Place_Name']: (float(place['Lat']), float(place['Long']))
            for place in day_places.values()
        }
        route_info = solve_tsp(places_with_coords)
        if route_info:
            optimized_routes.append(route_info)

    return jsonify({"selected_places": selected_places, "routes": optimized_routes})
