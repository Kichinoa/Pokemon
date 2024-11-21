import json
import requests
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
import pokebase as pb


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
    root = tk.Tk()
    root.title("Pokedex")
    root.geometry("400x600")
    root.configure(bg="#FF0000")
    return root


def create_border_frame(root):
    border_frame = tk.Frame(root, bg="#8B0000", bd=10)
    border_frame.place(relx=0.5, rely=0.5, anchor="center",width=380, height=580)
    return border_frame

def create_screen_frame(border_frame):
    screen_frame = tk.Frame(border_frame, bg="black", bd=10)
    screen_frame.place(relx=0.5, rely=0.3, anchor="center", width=300, height=200)
    return screen_frame


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


def create_joystick_frame(border_frame, screen_frame, image_id):
    joystick_frame = tk.Frame(border_frame, bg="#FF0000")
    joystick_frame.place(relx=0.7, rely=0.85, anchor="center")

    def previous_image():
        nonlocal image_id
        image_id -= 1
        for widget in screen_frame.winfo_children():
            widget.destroy()
        display_images(screen_frame, image_id)

    def next_image():
        nonlocal image_id
        image_id += 1
        for widget in screen_frame.winfo_children():
            widget.destroy()
        display_images(screen_frame, image_id)

    btn_left = ttk.Button(joystick_frame, text="Previous", command=previous_image)
    btn_left.grid(row=0, column=0, padx=5, pady=5)

    btn_right = ttk.Button(joystick_frame, text="Next", command=next_image)
    btn_right.grid(row=0, column=1, padx=5, pady=5)





def add_decorative_elements(border_frame):
    decorative_frame = tk.Frame(border_frame, bg="#FF4500", bd=2)
    decorative_frame.place(relx=0.5, rely=0.1, anchor="center", width=100, height=20)

    decorative_label = tk.Label(decorative_frame, text="Pokedex", bg="#FF4500", fg="white", font=("Helvetica", 12, "bold"))
    decorative_label.pack()
    
def create_info_box(border_frame):
    info_frame = tk.Frame(border_frame, bg="black", bd=2, highlightbackground="green", highlightthickness=2)
    info_frame.place(relx=0.1, rely=0.85, anchor="sw", width=150, height=150)  # Position it at the bottom left
    return info_frame

def update_info_box(info_frame, pokemon_data):
    for widget in info_frame.winfo_children():
        widget.destroy()

    name_label = tk.Label(info_frame, text=f"Name: {pokemon_data['name']}", bg="black", fg="green", font=("Courier", 10))
    name_label.pack(anchor="w")

    height_label = tk.Label(info_frame, text=f"Height: {pokemon_data['height']}", bg="black", fg="green", font=("Courier", 10))
    height_label.pack(anchor="w")

    weight_label = tk.Label(info_frame, text=f"Weight: {pokemon_data['weight']}", bg="black", fg="green", font=("Courier", 10))
    weight_label.pack(anchor="w")

    types = ', '.join([t['type']['name'] for t in pokemon_data['types']])
    types_label = tk.Label(info_frame, text=f"Types: {types}", bg="black", fg="green", font=("Courier", 10))
    types_label.pack(anchor="w")


def read_file(path):
    with open(path, "r") as f:
        return f.read()
    
filename ="Pokedex.json"

def fetch_pokemon_data(pokemon_name):
    pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
    if pokemon.status_code == 200:
        data = pokemon.json()
        with open("Pokedex.json", "w") as pokedex:
            json.dump(data, pokedex)
        return data
    else:
        messagebox.showerror("Error", "Pokémon not found. Please enter a valid name.")
        return None


def main():
    root = create_main_window()
    border_frame = create_border_frame(root)
    screen_frame = create_screen_frame(border_frame)
    info_frame = create_info_box(border_frame)
    image_id = 1
    display_images(screen_frame, image_id)
    create_joystick_frame(border_frame, screen_frame, image_id)
    add_decorative_elements(border_frame)

    def on_submit():
        pokemon_name = entry.get().lower()
        pokemon_data = fetch_pokemon_data(pokemon_name)
        if pokemon_data is not None:
            image_id = pokemon_data["id"]
            for widget in  screen_frame.winfo_children():
                widget.destroy()
            display_images(screen_frame, image_id)

            update_info_box(info_frame, pokemon_data)

  

    entry = tk.Entry(border_frame)
    entry.place(relx=0.71, rely=0.7, anchor="center")

    submit_button = ttk.Button(border_frame, text="Submit", command=on_submit)
    submit_button.place(relx=0.71, rely=0.75, anchor="center")

    root.mainloop()


if __name__ == "__main__":
    main()