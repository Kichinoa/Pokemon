import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from io import BytesIO

# Initialize a variable to store the current Pokémon ID
current_pokemon_id = 1  # Starting with Pokémon ID 1 (Bulbasaur)

def load_local_image(image_path, size=(80, 30)):
    """Load an image from a local path, resize it, and convert it to Tkinter PhotoImage."""
    try:
        img = Image.open(image_path)  # Open the image from the local file system
        img = img.resize(size, Image.LANCZOS)  # Resize image to fit
        return ImageTk.PhotoImage(img)  # Return Tkinter compatible PhotoImage
    except FileNotFoundError:
        print(f"Local image not found at {image_path}.")
        return None
    except Exception as e:
        print(f"Error loading local image: {e}")
        return None

def load_image_from_url(url, size=(80, 80)):
    """Load an image from a URL, resize it, and return as a Tkinter PhotoImage."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we got a valid response
        img_data = response.content
        img = Image.open(BytesIO(img_data))  # Convert image data to a PIL Image object
        img = img.resize(size, Image.LANCZOS)  # Resize image
        return ImageTk.PhotoImage(img)  # Return Tkinter compatible PhotoImage
    except requests.exceptions.RequestException as e:
        print(f"Error loading image from URL: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def create_main_window():
    """Creates the main Tkinter window with a background image."""
    root = tk.Tk()
    root.title("Pokedex")
    root.geometry("810x600")

    # Load and set the background image
    background_image_path = "D:/pokemonpy/img/pokedex.jpg"  # Change this to your correct path
    background_image = Image.open(background_image_path)
    background_image = background_image.resize((810, 600), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    
    # Place the background image
    background_label = tk.Label(root, image=background_photo)
    background_label.image = background_photo  # Keep a reference to avoid garbage collection
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    return root

def display_images(screen_frame, image_id):
    """Display both normal and shiny sprites for a Pokémon using separate frames for each sprite."""
    
    # Create a Frame for the normal sprite
    normal_sprite_frame = tk.Frame(screen_frame, bg="#b7eaff", bd=0)  # Set the background color to #b7eaff
    normal_sprite_frame.place(relx=0.66, rely=0.5, anchor="center")  # Position the normal sprite frame
    
    # Create a Frame for the shiny sprite
    shiny_sprite_frame = tk.Frame(screen_frame, bg="#b7eaff", bd=0)  # Set the background color to #b7eaff
    shiny_sprite_frame.place(relx=0.87, rely=0.81, anchor="center")  # Position the shiny sprite frame next to the normal sprite
    
    # URLs for the normal and shiny sprites
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{image_id}.png"
    shiny_image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/{image_id}.png"
    
    # Load the normal sprite
    normal_image = load_image_from_url(image_url, size=(200, 200))
    if normal_image:
        normal_image_label = tk.Label(normal_sprite_frame, image=normal_image, bg="#b7eaff")  # Set background to match frame
        normal_image_label.image = normal_image  # Keep reference to avoid garbage collection
        normal_image_label.pack(padx=10)  # Use pack to center the sprite inside the frame
    else:
        # Display placeholder text if normal sprite is not available
        normal_image_label = tk.Label(normal_sprite_frame, text="Normal Sprite not available", bg="#b7eaff", fg="black")
        normal_image_label.pack(padx=10)

    # Load the shiny sprite
    shiny_image = load_image_from_url(shiny_image_url, size=(100, 100))
    if shiny_image:
        shiny_image_label = tk.Label(shiny_sprite_frame, image=shiny_image, bg="#b7eaff")  # Set background to match frame
        shiny_image_label.image = shiny_image  # Keep reference to avoid garbage collection
        shiny_image_label.pack(padx=10)  # Use pack to center the sprite inside the frame
    else:
        # Display placeholder text if shiny sprite is not available
        shiny_image_label = tk.Label(shiny_sprite_frame, text="Shiny Sprite not available", bg="#b7eaff", fg="black")
        shiny_image_label.pack(padx=10)

    # Keep references to avoid garbage collection issues
    screen_frame.image_refs = [normal_image, shiny_image]

def update_info_box(root, pokemon_data):
    """Displays the Pokémon's information below the image."""
    # Clear any existing info labels
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label) and widget != root.children['!label']:
            widget.destroy()

    # Display ID and name (ID comes before name)
    name_label = tk.Label(root, text=f"ID: {pokemon_data['id']} - {pokemon_data['name'].title()}", bg="#95e2fe", fg="black", font=("Courier", 24, "bold"))
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
    stat_y_position = 0.5
    for stat_name, stat_value in stats.items():
        stat_label = tk.Label(root, text=f"{stat_name}: {stat_value}", bg="#95e2fe", fg="black", font=("Courier", 12))
        stat_label.place(relx=0.15, rely=stat_y_position, anchor="center")
        stat_y_position += 0.05  # Increment Y position for next stat


def fetch_pokemon_data(pokemon_id):
    """Fetches data for a Pokémon by ID."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        pokemon_data = response.json()
        return {
            'name': pokemon_data['name'],
            'height': pokemon_data['height'],
            'weight': pokemon_data['weight'],
            'types': pokemon_data['types'],
            'stats': pokemon_data['stats'],
            'id': pokemon_id
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for Pokémon ID {pokemon_id}: {e}")
        return None

def on_next_button(root):
    """Show the next Pokémon."""
    global current_pokemon_id
    current_pokemon_id += 1  # Increment to next Pokémon ID
    pokemon_data = fetch_pokemon_data(current_pokemon_id)
    if pokemon_data:
        display_images(root, current_pokemon_id)
        update_info_box(root, pokemon_data)

def on_previous_button(root):
    """Show the previous Pokémon."""
    global current_pokemon_id
    if current_pokemon_id > 1:
        current_pokemon_id -= 1  # Decrement to previous Pokémon ID
        pokemon_data = fetch_pokemon_data(current_pokemon_id)
        if pokemon_data:
            display_images(root, current_pokemon_id)
            update_info_box(root, pokemon_data)

def create_navigation_buttons(root):
    """Create the Next and Previous buttons for navigation."""
    next_button = tk.Button(root, text="Next", command=lambda: on_next_button(root), font=("Courier", 16), bg="#95e2fe")
    next_button.place(relx=0.65, rely=0.95, anchor="center")  # Position it on the right
    
    prev_button = tk.Button(root, text="Previous", command=lambda: on_previous_button(root), font=("Courier", 16), bg="#95e2fe")
    prev_button.place(relx=0.5, rely=0.95, anchor="center")  # Position it on the left

def on_search_button(root, search_entry):
    """Handle the search functionality."""
    global current_pokemon_id
    pokemon_name = search_entry.get().lower()  # Get the name from the search entry
    if pokemon_name:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for successful response
            pokemon_data = response.json()
            current_pokemon_id = pokemon_data['id']  # Update the global current_pokemon_id
            display_images(root, current_pokemon_id)
            update_info_box(root, pokemon_data)
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "Pokemon not found.")
    else:
        messagebox.showwarning("Input Error", "Please enter a Pokemon name.")

def create_search_bar(root):
    """Create the search bar and button."""
    search_entry = tk.Entry(root, font=("Courier", 12), bg="#d3e5f0")
    search_entry.place(relx=0.3, rely=0.87, anchor="center")
    
    search_button = tk.Button(root, text="Search", command=lambda: on_search_button(root, search_entry), font=("Courier", 16), bg="#95e2fe")
    search_button.place(relx=0.30, rely=0.95, anchor="center")

# Initialize and run the application
root = create_main_window()

# Create the search bar
create_search_bar(root)

# Display the first Pokémon initially
pokemon_data = fetch_pokemon_data(current_pokemon_id)
if pokemon_data:
    display_images(root, current_pokemon_id)
    update_info_box(root, pokemon_data)

# Add navigation buttons
create_navigation_buttons(root)

root.mainloop()
