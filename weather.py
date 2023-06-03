import requests
import config

def get_weather_info(location):
    # Replace YOUR_API_KEY with the API key from config.py
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={config.OPENWEATHER_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    # Check if the API returned an error message
    if data['cod'] != 200:
        return "Sorry, that location is not valid."
    
    # Extract relevant weather information from the response
    description = data['weather'][0]['description']
    temperature = data['main']['temp'] - 273.15  # Convert from Kelvin to Celsius
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed'] * 3.6  # Convert from m/s to km/h
    
    # Capitalize the first letter of the location
    location = location.capitalize()
    
    # Calculate the heat index if applicable
    if temperature > 27 and humidity > 40:
        heat_index = -8.784695 + 1.61139411*temperature + 2.33854883889*humidity - 0.14611605*temperature*humidity - 0.012308094*temperature**2 - 0.016424828*humidity**2 + 0.002211732*temperature**2*humidity + 0.00072546*temperature*humidity**2 - 0.000003582*temperature**2*humidity**2
        heat_index = round(heat_index, 1)
        heat_index_str = f", with a **heat index of {heat_index}°C**"
    else:
        heat_index_str = ""
    
    # Format the weather information into a string
    weather_info = f"Umm, the weather in **{location}** is **{description}**, with a temperature of **{temperature:.1f}°C**, humidity of **{humidity}%**, and wind speed of **{wind_speed:.1f} km/h** {heat_index_str}."
    
    # Generate a random message based on the temperature and wind speed
    if temperature <= 0:
        message = "Umm... it's freezing outside! Make sure to wear thick clothing to keep yourself warm."
    elif temperature <= 10:
        message = "It's... quite cold outside, don't forget to wear warm clothing."
    elif temperature <= 20:
        message = "The weather is... nice today, have a good day!"
    elif temperature <= 30:
        message = "It's getting... hot outside, make sure to stay hydrated."
    else:
        message = "It's... dangerously hot outside, try to stay indoors and keep yourself cool."
    
    # Determine the wind speed category and add a message if necessary
    if wind_speed >= 185:
        weather_info += " Oh... umm... a super typhoon is currently occurring, please take extreme precautions."
    elif wind_speed >= 118:
        weather_info += " Oh... umm... a typhoon is currently occurring, please take necessary precautions."
    elif wind_speed >= 89:
        weather_info += " There is... umm... a severe tropical storm in the area, please stay safe."
    elif wind_speed >= 62:
        weather_info += " A tropical storm is expected, please be prepared."
    elif wind_speed >= 39:
        weather_info += " Strong winds are expected, please be cautious."
    
    return weather_info + "\n\n" + message