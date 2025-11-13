from flask import Flask, render_template, request, jsonify, session
from weather import (
    get_current_weather, 
    get_weather_by_coordinates, 
    get_weather_forecast,
    search_cities,
    get_air_quality,
    convert_temperature,
    COUNTRY_CODES
)
from waitress import serve
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', countries=COUNTRY_CODES)

@app.route('/weather')
def get_weather():
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '')
    units = request.args.get('units', 'metric')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # Check for empty strings or string with only spaces
    if not city and not (lat and lon):
        city = "Kansas City"
    
    # Get country code if country name is provided
    country_code = None
    if country and country in COUNTRY_CODES:
        country_code = COUNTRY_CODES[country]
    elif country and len(country) == 2:
        country_code = country.upper()
    
    # Get weather data
    if lat and lon:
        try:
            weather_data = get_weather_by_coordinates(float(lat), float(lon), units)
        except ValueError:
            return render_template('city-not-found.html', error="Invalid coordinates")
    else:
        weather_data = get_current_weather(city, country_code, units)
    
    # City is not found by API
    if not weather_data.get('cod') == 200:
        return render_template('city-not-found.html', 
                             error=weather_data.get('message', 'City not found'))
    
    # Save to search history
    if 'search_history' not in session:
        session['search_history'] = []
    
    search_entry = {
        'city': weather_data['name'],
        'country': weather_data['sys']['country'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'temp': weather_data['main']['temp'],
        'units': units
    }
    
    # Add to history (keep last 10)
    session['search_history'].insert(0, search_entry)
    session['search_history'] = session['search_history'][:10]
    
    # Get air quality data
    air_quality = get_air_quality(weather_data['coord']['lat'], weather_data['coord']['lon'])
    
    # Determine temperature unit symbol
    temp_unit = '°C' if units == 'metric' else '°F' if units == 'imperial' else 'K'
    
    return render_template(
        "weather.html",
        title=weather_data["name"],
        country=weather_data["sys"]["country"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}",
        temp_unit=temp_unit,
        humidity=weather_data['main']['humidity'],
        pressure=weather_data['main']['pressure'],
        wind_speed=weather_data.get('wind', {}).get('speed', 0),
        wind_direction=weather_data.get('wind', {}).get('deg', 0),
        visibility=weather_data.get('visibility', 0) / 1000,  # Convert to km
        sunrise=datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M'),
        sunset=datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M'),
        coordinates={'lat': weather_data['coord']['lat'], 'lon': weather_data['coord']['lon']},
        air_quality=air_quality,
        units=units,
        countries=COUNTRY_CODES,
        search_history=session.get('search_history', [])
    )

@app.route('/forecast')
def get_forecast():
    city = request.args.get('city', '').strip()
    country = request.args.get('country', '')
    units = request.args.get('units', 'metric')
    days = int(request.args.get('days', 5))
    
    if not city:
        return render_template('city-not-found.html', error="City name required for forecast")
    
    # Get country code if country name is provided
    country_code = None
    if country and country in COUNTRY_CODES:
        country_code = COUNTRY_CODES[country]
    elif country and len(country) == 2:
        country_code = country.upper()
    
    forecast_data = get_weather_forecast(city, country_code, units, days)
    
    if not forecast_data.get('cod') == '200':
        return render_template('city-not-found.html', 
                             error=forecast_data.get('message', 'Forecast not available'))
    
    # Process forecast data
    daily_forecasts = []
    current_date = None
    daily_data = []
    
    for item in forecast_data['list']:
        date = datetime.fromtimestamp(item['dt']).date()
        
        if current_date != date:
            if daily_data:
                # Process previous day's data
                daily_forecasts.append(process_daily_forecast(daily_data, current_date))
            current_date = date
            daily_data = [item]
        else:
            daily_data.append(item)
    
    # Process last day
    if daily_data:
        daily_forecasts.append(process_daily_forecast(daily_data, current_date))
    
    temp_unit = '°C' if units == 'metric' else '°F' if units == 'imperial' else 'K'
    
    return render_template(
        "forecast.html",
        city=forecast_data['city']['name'],
        country=forecast_data['city']['country'],
        forecasts=daily_forecasts[:days],
        temp_unit=temp_unit,
        units=units,
        countries=COUNTRY_CODES
    )

def process_daily_forecast(daily_data, date):
    """Process hourly data into daily summary"""
    temps = [item['main']['temp'] for item in daily_data]
    descriptions = [item['weather'][0]['description'] for item in daily_data]
    
    # Find most common weather description
    most_common_desc = max(set(descriptions), key=descriptions.count)
    
    return {
        'date': date.strftime('%A, %B %d'),
        'min_temp': min(temps),
        'max_temp': max(temps),
        'description': most_common_desc.capitalize(),
        'icon': daily_data[len(daily_data)//2]['weather'][0]['icon'],  # Middle of day icon
        'humidity': sum(item['main']['humidity'] for item in daily_data) / len(daily_data),
        'wind_speed': sum(item.get('wind', {}).get('speed', 0) for item in daily_data) / len(daily_data)
    }

@app.route('/api/search_cities')
def api_search_cities():
    """API endpoint for city search autocomplete"""
    query = request.args.get('q', '').strip()
    if len(query) < 2:
        return jsonify([])
    
    cities = search_cities(query, limit=10)
    
    # Format cities for frontend
    formatted_cities = []
    for city in cities:
        formatted_cities.append({
            'name': city['name'],
            'country': city['country'],
            'state': city.get('state', ''),
            'lat': city['lat'],
            'lon': city['lon'],
            'display_name': f"{city['name']}, {city.get('state', '')}, {city['country']}".replace(', ,', ',').strip(',')
        })
    
    return jsonify(formatted_cities)

@app.route('/api/convert_temperature')
def api_convert_temperature():
    """API endpoint for temperature conversion"""
    temp = float(request.args.get('temp', 0))
    from_unit = request.args.get('from', 'celsius')
    to_unit = request.args.get('to', 'fahrenheit')
    
    converted_temp = convert_temperature(temp, from_unit, to_unit)
    
    return jsonify({
        'original': temp,
        'converted': round(converted_temp, 1),
        'from_unit': from_unit,
        'to_unit': to_unit
    })

@app.route('/history')
def search_history():
    """Display search history"""
    history = session.get('search_history', [])
    return render_template('history.html', history=history)

@app.route('/clear_history')
def clear_history():
    """Clear search history"""
    session['search_history'] = []
    return render_template('history.html', history=[], message="History cleared successfully")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)