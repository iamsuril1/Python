import tkinter as tk
from tkinter import messagebox
import requests
import random

LASTFM_API_KEY = '20589b30798bb2d372f6343cfde9a3b9'

def fetch_songs(mood):
    try:
        url = f'http://ws.audioscrobbler.com/2.0/?method=tag.gettoptracks&tag={mood}&api_key={LASTFM_API_KEY}&format=json&limit=5'
        response = requests.get(url)
        response.raise_for_status()
        tracks = response.json()['tracks']['track']
        return [f"{track['name']} - {track['artist']['name']}" for track in tracks]
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch songs: {e}")
        return []
    except KeyError:
        messagebox.showerror("Error", "Invalid API response format.")
        return []

def suggest_songs():
    mood = mood_var.get()
    if mood:
        try:
            suggested_songs = fetch_songs(mood)
            if suggested_songs:
                results_text.delete(1.0, tk.END)
                results_text.insert(tk.END, f"Suggested {mood.capitalize()} Songs:\n")
                for song in suggested_songs:
                    results_text.insert(tk.END, f"- {song}\n")
            else:
                results_text.delete(1.0, tk.END)
                results_text.insert(tk.END, "No songs found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showwarning("Warning", "Please select a mood")

# GUI setup
app = tk.Tk()
app.title("Mood-Based Song Suggestion")

# Mood selection radio buttons with icons (imaginary icons)
mood_var = tk.StringVar()
mood_options = [("😊 Happy", "happy"), ("😢 Sad", "sad"), ("😌 Relaxed", "relax"), ("💥 Energetic", "energetic")]

tk.Label(app, text="Select your mood:").pack(anchor=tk.W)
for text, value in mood_options:
    tk.Radiobutton(app, text=text, variable=mood_var, value=value).pack(anchor=tk.W)

# Button to suggest songs
tk.Button(app, text="Suggest Songs", command=suggest_songs).pack()

# Text widget to display results
results_text = tk.Text(app, width=50, height=10)
results_text.pack()

app.mainloop()
