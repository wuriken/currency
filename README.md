url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5' 
import requests
response = requests.get(url)
response.json()   