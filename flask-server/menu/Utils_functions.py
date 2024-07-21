import requests
from selenium import webdriver
import folium
import datetime
import time


def locationCoordinates():
	try:
		response = requests.get('https://ipinfo.io')
		data = response.json()
		loc = data['loc'].split(',')
		lat, long = float(loc[0]), float(loc[1])
		city = data.get('city', 'Unknown')
		state = data.get('region', 'Unknown')
		return lat, long, city, state
		# return lat, long
	except:
		# Displaying ther error message
		print("Internet Not avialable")
		# closing the program
		exit()

print("---------------GPS Using Python---------------\n")

lat, long, city, state = locationCoordinates()
print(f'the coordinates and location is: {lat}, {long}, {city}, {state}')
