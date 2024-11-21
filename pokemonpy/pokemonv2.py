import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO

def load_image(url):
    """Loads an image from a URL and converts it to a Tkinter PhotoImage."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        return ImageTk.PhotoImage(img)
    except requests.exceptions.RequestException as e:
        print(f"Error loading image: {e}")
        return None

def create_main_window():
    """Creates the main Tkinter window with a background image."""
    root = tk.Tk()
    root.title("Pokedex")
    root.geometry("400x600")

    # Load and set the background image
    background_image_path = "D:\pokemonpy\img\pokedex.jpg"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((400, 600), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    
    # Place the background image
    background_label = tk.Label(root, image=background_photo)
    background_label.image = background_photo  # Keep a reference to avoid garbage collection
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    return root

def display_pokemon_image(root, image_id):
    """Displays the Pokémon image on the main screen."""
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{image_id}.png"
    image = load_image(image_url)
    if image:
        image_label = tk.Label(root, image=image, bg=None)
        image_label.image = image
        image_label.place(relx=0.5, rely=0.25, anchor="center")
    else:
        image_label = tk.Label(root, text="Image not available", bg=None, fg="white")
        image_label.place(relx=0.5, rely=0.25, anchor="center")

def update_info_box(root, pokemon_data):
    """Displays the Pokémon's information below the image."""
    # Clear any existing info labels
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and widget != root.children['!label']:
            widget.destroy()

    # Display name
    name_label = tk.Label(root, text=f"{pokemon_data['name'].title()}", bg="#95e2fe", fg="black", font=("Courier", 16, "bold"))
    name_label.place(relx=0.2, rely=0.14, anchor="center")

    # Display height and weight
    height_label = tk.Label(root, text=f"Height: {pokemon_data['height']} m", bg="#95e2fe", fg="black", font=("Courier", 10))
    height_label.place(relx=0.5, rely=0.6, anchor="center")

    weight_label = tk.Label(root, text=f"Weight: {pokemon_data['weight']} kg", bg="#95e2fe", fg="black", font=("Courier", 10))
    weight_label.place(relx=0.5, rely=0.65, anchor="center")

    # Display type(s)
    types = ', '.join([t['type']['name'].title() for t in pokemon_data['types']])
    types_label = tk.Label(root, text=f"Type: {types}", bg="#95e2fe", fg="black", font=("Courier", 10))
    types_label.place(relx=0.5, rely=0.7, anchor="center")

        # Display stats
    stats = {
        "Attack": pokemon_data['stats'][1]['base_stat'],
        "Defense": pokemon_data['stats'][2]['base_stat'],
        "Special Attack": pokemon_data['stats'][3]['base_stat'],
        "Special Defense": pokemon_data['stats'][4]['base_stat'],
        "Speed": pokemon_data['stats'][5]['base_stat']
    }

    # Position for displaying stats
    stat_y_position = 0.75  # Starting position for stats display
    for stat_name, stat_value in stats.items():
        stat_label = tk.Label(root, text=f"{stat_name}: {stat_value}", bg="#95e2fe", fg="black", font=("Courier", 10))
        stat_label.place(relx=0.5, rely=stat_y_position, anchor="center")
        stat_y_position += 0.05  # Increment the position for the next stat

def fetch_pokemon_data(pokemon_name):
    """Fetches Pokémon data from the PokeAPI."""
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Pokémon not found: {e}")
        return None

def main():
    # Create main window and background
    root = create_main_window()
    
    # Input box for searching Pokémon
    entry = tk.Entry(root, font=("Courier", 10))
    entry.place(relx=0.5, rely=0.8, anchor="center", width=120)

    # Search button
    def on_submit():
        pokemon_name = entry.get()
        pokemon_data = fetch_pokemon_data(pokemon_name)
        if pokemon_data:
            display_pokemon_image(root, pokemon_data["id"])
            update_info_box(root, pokemon_data)

    submit_button = ttk.Button(root, text="Search", command=on_submit)
    submit_button.place(relx=0.5, rely=0.85, anchor="center")

    root.mainloop()

if __name__ == "__main__":
    main()
