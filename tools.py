import requests

def get_weather(city = "kathmandu"):
    try:
        url = f"https://wttr.in/{city}?format=3"
        res = requests.get(url)
        if res.status_code == 200:
            return res.text.strip()
        else:
            return f"Error: Unable to fetch weather data for {city}. Status code: {res.status_code}"
    except Exception as e:
        return f"weather tool error:{str(e)}"