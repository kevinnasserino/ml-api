from flask import Flask, request, jsonify
import tensorflow as tf
import pandas as pd
from tsp import solve_tsp
from cbf import recommend
from tensorflow.keras.models import load_model

app = Flask(__name__)

# Load pre-trained model
cbf_model = load_model('models/cbf_model.h5')

# Load dataset
places_df = pd.read_csv('dataset/tourismkelana_fixed.csv')

@app.route('/itinerary', methods=['POST'])
def generate_itinerary():
    """
    Generate a complete itinerary with recommendations and optimized route.
    """
    data = request.json
    city = data.get('city')
    price_category = data.get('price_category')
    time_slot = data.get('time_slot', 'morning')
    top_n = data.get('top_n', 3)

    try:
        # Get recommended places
        recommendations = recommend(city, price_category, time_slot, top_n)
        if isinstance(recommendations, str):  # No results
            return jsonify({'status': 'error', 'message': recommendations}), 404

        # Extract places for route optimization
        places = {}
        for _, row in recommendations.iterrows():
            places[row['Place_Name']] = [row['Latitude'], row['Longitude']]

        # Optimize route
        route_info = solve_tsp(places)

        # Build itinerary response
        itinerary = []
        for idx, place in enumerate(route_info['route']):
            place_data = recommendations[recommendations['Place_Name'] == place].iloc[0]
            itinerary.append({
                "Day": (idx // 3) + 1,
                "Time_Slot": time_slot,
                "Place_Name": place_data['Place_Name'],
                "Category": place_data['Category'],
                "Coordinates": [place_data['Latitude'], place_data['Longitude']],
                "Rating": place_data['Rating'],
                "Price": place_data['Price_Category']
            })

        # Return response
        return jsonify({
            "status": "success",
            "itinerary": itinerary,
            "total_distance": route_info['total_distance']
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
