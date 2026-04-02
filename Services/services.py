import requests
from sklearn.linear_model import LinearRegression
import numpy as np

API_KEY = "579b464db66ec23bdd0000015d440c734be241766ea3b5f7a015df7e"

'''def get_prices_data(crop=None, state=None, district=None):
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 1000
    }

    # API Filters
    if state:
        params["filters[state.keyword]"] = state

    if district:
        params["filters[district.keyword]"] = district

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        result = []

        for item in data.get("records", []):
            crop_name = item.get("commodity", "")
            state_name = item.get("state", "")
            district_name = item.get("district", "")
            market = item.get("market", "")
            price = item.get("modal_price", "")

            # Crop filter (local filter)
            if crop and crop.lower() not in crop_name.lower():
                continue

            result.append({
                "crop": crop_name,
                "state": state_name,
                "district": district_name,
                "market": market,
                "price": price
            })

        return result

    except Exception as e:
        print("ERROR:", e)
        return []  


# 🤖 AI PREDICTION
def predict_price(data):
    try:
        prices = []

        for item in data:
            try:
                prices.append(int(item["price"]))
            except:
                continue

        if len(prices) < 2:
            return "Not enough data"

        X = np.array(range(len(prices))).reshape(-1,1)
        y = np.array(prices)

        model = LinearRegression()
        model.fit(X, y)

        next_day = np.array([[len(prices)]])
        pred = model.predict(next_day)

        return int(pred[0])

    except:
        return "Error"'''

def get_prices_data(crop=None, state=None, district=None):
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 1000,

        # 🔥 FORCE MAHARASHTRA FROM API
        "filters[state]": "Maharashtra"
    }

    # Optional district filter
    if district:
        params["filters[district]"] = district

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        result = []

        for item in data.get("records", []):
            crop_name = item.get("commodity", "")
            state_name = item.get("state", "")
            district_name = item.get("district", "")
            market = item.get("market", "")
            price = item.get("modal_price", "")

            # 🔍 Crop filter
            if crop and crop.lower() not in crop_name.lower():
                continue

            # 🔥 DOUBLE SAFETY CHECK (IMPORTANT)
            if state_name.strip() != "Maharashtra":
                continue

            result.append({
                "crop": crop_name,
                "state": state_name,
                "district": district_name,
                "market": market,
                "price": price
            })

        # 🔥 FALLBACK (if API still fails)
        if not result:
            return [
                {"crop": "Onion", "state": "Maharashtra", "district": "Pune", "market": "Pune", "price": "1500"},
                {"crop": "Wheat", "state": "Maharashtra", "district": "Nashik", "market": "Nashik", "price": "2100"}
            ]

        return result

    except Exception as e:
        print("ERROR:", e)
        return [
            {"crop": "Onion", "state": "Maharashtra", "district": "Pune", "market": "Pune", "price": "1500"},
            {"crop": "Wheat", "state": "Maharashtra", "district": "Nashik", "market": "Nashik", "price": "2100"}
        ]
