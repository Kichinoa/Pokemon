import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO

def load_local_image(image_path, size=(80, 30)):
    """Loads an image from a local path, resizes it, and converts it to a Tkinter PhotoImage."""
    try:
        img = Image.open(image_path)  # Open image from local path
        img = img.resize(size, Image.LANCZOS)  # Resize the image
        return ImageTk.PhotoImage(img)  # Convert to Tkinter compatible format
    except Exception as e:
        print(f"Error loading image: {e}")
        return None



def load_image(url):
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
    root.geometry("810x600")

    # Load and set the background image
    background_image_path = "D:\pokemonpy\img\pokedex.jpg"
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((810, 600), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    
    # Place the background image
    background_label = tk.Label(root, image=background_photo)
    background_label.image = background_photo  # Keep a reference to avoid garbage collection
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    return root

def display_images(screen_frame, image_id):
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{image_id}.png"
    image = load_image(image_url)
    if image:
        image_label = tk.Label(screen_frame, image=image, bg="black")
        image_label.image = image
        image_label.pack(side="left", expand=True)
    else:
        image_label = tk.Label(screen_frame, text="Image not available", bg="black", fg="white")
        image_label.pack(side="left", expand=True)

    image_url2 = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{image_id}.png"
    image2 = load_image(image_url2)
    if image2:
        image_label2 = tk.Label(screen_frame, image=image2, bg="black")
        image_label2.image = image2
        image_label2.pack(side="left", expand=True)
    else:
        image_label2 = tk.Label(screen_frame, text="Image not available", bg="black", fg="white")
        image_label2.pack(side="left", expand=True)

def update_info_box(root, pokemon_data):
    """Displays the Pokémon's information below the image."""
    # Clear any existing info labels
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and widget != root.children['!label']:
            widget.destroy()

    # Display name
    name_label = tk.Label(root, text=f"{pokemon_data['name'].title()}", bg="#95e2fe", fg="black", font=("Courier", 24, "bold"))
    name_label.place(relx=0.2, rely=0.14, anchor="center")

    # Display height and weight
    height_label = tk.Label(root, text=f"Height: {pokemon_data['height']} m", bg="#95e2fe", fg="black", font=("Courier", 16))
    height_label.place(relx=0.15, rely=0.4, anchor="center")

    weight_label = tk.Label(root, text=f"Weight: {pokemon_data['weight']} kg", bg="#95e2fe", fg="black", font=("Courier", 16))
    weight_label.place(relx=0.15, rely=0.45, anchor="center")

    # Display types as images next to each other
    types = pokemon_data['types']
    type_images = []  # List to store the type image labels

    # Base X position for displaying types
    type_x_position = 0.6  # Starting position for types (relx)

    for t in types:
        type_name = t['type']['name']
        # Assuming you have the type images in the "types" folder with filenames like "fire.png", "water.png", etc.
        image_path = f"D:/pokemonpy/img/types/{type_name}.png"  # Adjust path accordingly
        type_image = load_local_image(image_path, size=(70, 50))  # Resize the type images
        if type_image:
            type_label = tk.Label(root, image=type_image, bg="#95e2fe")
            type_label.image = type_image  # Keep a reference to avoid garbage collection
            type_label.place(relx=type_x_position, rely=0.08, anchor="center")
            type_x_position += 0.1  # Increment the X position for the next type image (horizontal spacing)

    # Display stats
    stats = {
        "Attack": pokemon_data['stats'][1]['base_stat'],
        "Defense": pokemon_data['stats'][2]['base_stat'],
        "Special Attack": pokemon_data['stats'][3]['base_stat'],
        "Special Defense": pokemon_data['stats'][4]['base_stat'],
        "Speed": pokemon_data['stats'][5]['base_stat']
    }

    # Position for displaying stats
    stat_y_position = 0.5  # Start after the last type image
    for stat_name, stat_value in stats.items():
        stat_label = tk.Label(root, text=f"{stat_name}: {stat_value}", bg="#95e2fe", fg="black", font=("Courier", 16))
        stat_label.place(relx=0.15, rely=stat_y_position, anchor="center")
        stat_y_position += 0.05  # Increment the position for the next stat


def create_search_button(root, x, y, width, height, text, command):
    """Creates an oval button using the Canvas widget."""
    canvas = tk.Canvas(root, width=width, height=height, bg="#53a3ff", bd=0, highlightthickness=0)
    # Draw an oval
    canvas.create_oval(5, 5, width - 5, height - 5, fill="#ff4081", outline="#ff4081", width=5)
    # Place text over the oval
    canvas.create_text(width // 2, height // 2, text=text, fill="white", font=("Helvetica", 12, "bold"))
    
    # Bind the click event to the button functionality
    canvas.place(x=x, y=y)
    canvas.bind("<Button-1>", lambda event: command())
    
    return canvas

def on_submit(entry, root):
    """Handles the search button press."""
    pokemon_name = entry.get().strip()
    if not pokemon_name:
        messagebox.showwarning("Input Error", "Please enter a Pokémon name.")
        return
    pokemon_data = fetch_pokemon_data(pokemon_name)
    if pokemon_data:
        display_images(root, pokemon_data["id"])
        update_info_box(root, pokemon_data)

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
    
    entry = ttk.Entry(root, font=("Helvetica", 12), width=20)
    entry.place(relx=0.3, rely=0.87, anchor="center")

    create_search_button(root, x=170, y=550, width=150, height=40, text="Search", command=lambda: on_submit(entry, root))


    root.mainloop()

if __name__ == "__main__":
    main()
