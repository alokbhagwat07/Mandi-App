from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Services.services import  get_prices_data
from flask import Flask, render_template, jsonify, request
#from Services.services import  get_maharashtra_data

app = FastAPI(
    title="VajraStream API 🚀",
    description="Smart Mandi Price & Analysis System",
    version="1.0"
)

templates = Jinja2Templates(directory="templates")

# Serve static files(logo)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request}
    )

'''@app.get("/states")
def states_api():
    return get_states()
@app.get("/prices")
def prices_api(state: str = None):
    return get_data(state)'''


@app.get("/prices")
def get_prices(crop: str = None, state: str = None, district: str = None):
   return get_prices_data(crop, state, district)

#@app.get("/prices")
#def prices_api():
 #   return get_maharashtra_data()


@app.get("/prices-page", response_class=HTMLResponse)
def prices_page(request: Request):
    return templates.TemplateResponse(
        request,
        "prices.html",
        {"request": request}
    )

@app.get("/analysis-page", response_class=HTMLResponse)
def analysis_page(request: Request):
    data = get_prices_data()  # all data
    return templates.TemplateResponse(
        request,
        "analysis.html",
        {"request": request, "data": data}
    )

# 🔹 DASHBOARD PAGE
@app.get("/dashboard-page", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request,
        "dashboard.html", {"request": request})

@app.get("/dashboard-data")
def dashboard_data():

    data = get_prices_data()

    output = []

    for d in data:
        try:
            output.append({
                "crop": d.get("crop") or d.get("commodity"),
                "district": d.get("district"),
                "market": d.get("market"),
                "price": int(d.get("price") or d.get("modal_price") or 0)
            })
        except:
            continue

    return output

