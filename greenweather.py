import requests
from datetime import datetime, timedelta
import pytz

USERNAME = ''
PASSWORD = ''

def fetch_weather_data():
    base_url = 'https://api.meteomatics.com/'
    valid_datetime = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    parameters = 't_2m:C,precip_24h:mm,sunset:sql'
    location = ''
    # The location uses GPS data (can be collected from Google Maps)
    data_format = 'json'

    url = f'{base_url}{valid_datetime}/{parameters}/{location}/{data_format}?model=mix'

    response = requests.get(url, auth=(USERNAME, PASSWORD))

    # Used to check the json response
    #print('Response Status Code:', response.status_code)
    #print('Response Content:', response.content.decode('utf-8'))


    if response.status_code == 200:
        return response.json()
    else:
        print('Error fetching weather data:', response.status_code)
        return None

def get_current_temperature(data):
    temperature = data['data'][0]['coordinates'][0]['dates'][0]['value']
    return temperature

def get_rain_last_24_hours(data):
    rain = data['data'][1]['coordinates'][0]['dates'][0]['value']
    return rain

def get_sunset_time(data):
    sunset = data['data'][2]['coordinates'][0]['dates'][0]['value']
    return sunset

weather_data = fetch_weather_data()

if weather_data:
    temperature = get_current_temperature(weather_data)
    rain_last_24_hours = get_rain_last_24_hours(weather_data)
    sunset_time = get_sunset_time(weather_data)

    # Convert sunset time to datetime object
    sunset_datetime = datetime.fromisoformat(sunset_time[:-1])

    # Convert to Denmark timezone
    watering_time = sunset_datetime - timedelta(minutes=45) + timedelta(minutes=120)

    if temperature > 18 and rain_last_24_hours < 2:
        print('Yes, you should water the garden tonight.')
        print('Watering time:', watering_time.strftime('%H:%M'))
    else:
        print('No, you do not need to water the garden tonight.')