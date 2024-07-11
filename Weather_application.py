import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

def get_weather(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data

def get_weather_and_display():
    city = city_entry.get()
    api_key = '9ae92a0734944b7ea45822aad48cbf55'  
    
    weather_data = get_weather(city, api_key)
    
    if weather_data['cod'] == 200:
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        icon_name = weather_data['weather'][0]['icon']
        
        result_label.config(text=f"Weather in {city}: \nTemperature: {temperature} °C\nHumidity: {humidity}%\nDescription: {description}")
        
        load_weather_icon(icon_name)
    else:
        messagebox.showerror("Error", f"Error: {weather_data['message']}")

def load_weather_icon(icon_name):
    icon_url = f"http://openweathermap.org/img/w/{icon_name}.png"
    icon_response = requests.get(icon_url, stream=True)
    if icon_response.status_code == 200:
        with open("weather_icon.png", 'wb') as f:
            f.write(icon_response.content)
        
        weather_icon = Image.open("weather_icon.png")
        weather_icon = weather_icon.resize((100, 100), Image.LANCZOS)
        weather_icon = ImageTk.PhotoImage(weather_icon)
        
        icon_label.config(image=weather_icon)
        icon_label.image = weather_icon
    else:
        messagebox.showerror("Error", "Failed to load weather icon")

root = tk.Tk()
root.title("Weather Application")
root.configure(bg="#f0f0f0")

title_label = tk.Label(root, text="Weather Application", font=("Arial", 20), bg="#f0f0f0")
title_label.pack(pady=20)

city_label = tk.Label(root, text="Enter city:", font=("Arial", 12), bg="#f0f0f0")
city_label.pack()

city_entry = tk.Entry(root, width=30, font=("Arial", 12))
city_entry.pack(pady=10)

get_weather_button = tk.Button(root, text="Get Weather", font=("Arial", 12), command=get_weather_and_display)
get_weather_button.pack()

result_label = tk.Label(root, text="", font=("Arial", 12), wraplength=400, justify="left", bg="#f0f0f0")
result_label.pack(pady=20)

icon_label = tk.Label(root, bg="#f0f0f0")
icon_label.pack(pady=10)

root.mainloop()
