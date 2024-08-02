import random
import string
import tkinter as tk
from tkinter import messagebox

# Common two-letter words
two_letter_words = ["fr", "to", "go", "at", "by", "do", "he", "if", "in", "is", "it", "me", "no", "of", "on", "or", "so", "up", "us", "we"]

# Function to generate a unique username based on criteria
def generate_username(criteria, length):
    while True:
        if criteria == "letters_numbers_underscore":
            username = ''.join(random.choices(string.ascii_lowercase + string.digits + '_', k=length))
        elif criteria == "letters_numbers":
            username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        elif criteria == "numbers_underscore":
            username = ''.join(random.choices(string.digits + '_', k=length))
        elif criteria == "numbers":
            username = ''.join(random.choices(string.digits, k=length))
        elif criteria == "letters_underscore":
            username = ''.join(random.choices(string.ascii_lowercase + '_', k=length))

        # Insert a common two-letter word at a random position
        if length > 2:
            word = random.choice(two_letter_words)
            pos = random.randint(0, length - 2)
            username = username[:pos] + word + username[pos + 2:]
        
        # Ensure the username does not start or end with '_'
        if username[0] == '_' or username[-1] == '_':
            continue

        # Ensure the username is unique
        if username in generated_usernames:
            continue

        generated_usernames.add(username)
        return username

# Function to handle the generate button click event
def on_generate(criteria):
    length = name_length.get()
    new_username = generate_username(criteria, length)
    root.clipboard_clear()
    root.clipboard_append(new_username)
    messagebox.showinfo("Generated", f"Generated username: '{new_username}'\nCopied to clipboard!")

# Function to handle the paste button click event
def on_paste(section):
    username = root.clipboard_get()
    section.insert(tk.END, username + '\n')
    section.yview(tk.END)

# Function to save untaken usernames to a file
def save_usernames():
    try:
        with open('untaken_usernames.txt', 'w') as file:
            for username in untaken_usernames:
                file.write(username + '\n')
        print("Usernames saved successfully.")  # Debugging line
        messagebox.showinfo("Saved", "Untaken usernames have been saved to 'untaken_usernames.txt'")
    except Exception as e:
        print(f"Error saving usernames: {e}")  # Debugging line
        messagebox.showerror("Error", f"An error occurred while saving: {e}")

# Function to load untaken usernames from a file
def load_usernames():
    try:
        with open('untaken_usernames.txt', 'r') as file:
            for line in file:
                username = line.strip()
                if username:
                    untaken_usernames.add(username)
        update_untaken_display()
        print("Usernames loaded successfully.")  # Debugging line
        messagebox.showinfo("Loaded", "Untaken usernames have been loaded from 'untaken_usernames.txt'")
    except FileNotFoundError:
        print("No saved usernames found. Starting fresh.")  # Debugging line
        messagebox.showwarning("Warning", "No saved usernames found. Starting fresh.")
    except Exception as e:
        print(f"Error loading usernames: {e}")  # Debugging line
        messagebox.showerror("Error", f"An error occurred while loading: {e}")

# Function to update the display of untaken usernames
def update_untaken_display():
    untaken_text.delete(1.0, tk.END)
    for username in untaken_usernames:
        untaken_text.insert(tk.END, username + '\n')

# Set of already generated usernames
generated_usernames = set()
untaken_usernames = set()

# Create the main window
root = tk.Tk()
root.title("Username Generator")

# Create sections for each criteria
sections = {
    "letters_numbers_underscore": "Letters, Numbers, and Underscore",
    "letters_numbers": "Letters and Numbers",
    "numbers_underscore": "Numbers and Underscore",
    "numbers": "Numbers",
    "letters_underscore": "Letters and Underscore"
}

frames = {}
text_widgets = {}

for criteria, label in sections.items():
    frame = tk.LabelFrame(root, text=label)
    frame.pack(fill="both", expand="yes", padx=10, pady=5)
    text = tk.Text(frame, height=5)
    text.pack(fill="both", expand="yes")
    frames[criteria] = frame
    text_widgets[criteria] = text

lnu_text = text_widgets["letters_numbers_underscore"]
ln_text = text_widgets["letters_numbers"]
nu_text = text_widgets["numbers_underscore"]
n_text = text_widgets["numbers"]
lu_text = text_widgets["letters_underscore"]

# Untaken Usernames Section
untaken_frame = tk.LabelFrame(root, text="Untaken Usernames")
untaken_frame.pack(fill="both", expand="yes", padx=10, pady=5)
untaken_text = tk.Text(untaken_frame, height=10)
untaken_text.pack(fill="both", expand="yes")

# Menu section
menu_frame = tk.LabelFrame(root, text="Menu")
menu_frame.pack(fill="x", padx=10, pady=5)

# Auto-scroll button
auto_scroll_var = tk.BooleanVar()
auto_scroll_button = tk.Checkbutton(menu_frame, text="Auto Scroll", variable=auto_scroll_var)
auto_scroll_button.pack(side="left", padx=10)

# Name length spinbox
name_length_label = tk.Label(menu_frame, text="Name Length:")
name_length_label.pack(side="left", padx=10)
name_length = tk.IntVar(value=5)
name_length_spinbox = tk.Spinbox(menu_frame, from_=3, to=10, textvariable=name_length)
name_length_spinbox.pack(side="left", padx=10)

# Create a button to generate a new username for each section
buttons_frame = tk.Frame(root)
buttons_frame.pack(fill="x", padx=10, pady=5)

for criteria, label in sections.items():
    button = tk.Button(buttons_frame, text=f"Generate {label}", command=lambda c=criteria: on_generate(c))
    button.pack(side="left", padx=5)

# Create a button to paste the username into each section
paste_buttons_frame = tk.Frame(root)
paste_buttons_frame.pack(fill="x", padx=10, pady=5)

for criteria, label in sections.items():
    button = tk.Button(paste_buttons_frame, text=f"Paste to {label}", command=lambda t=text_widgets[criteria]: on_paste(t))
    button.pack(side="left", padx=5)

# Create buttons to save and load untaken usernames
save_button = tk.Button(root, text="Save Untaken Usernames", command=save_usernames)
save_button.pack(pady=5)

load_button = tk.Button(root, text="Load Untaken Usernames", command=load_usernames)
load_button.pack(pady=5)

# Run the application
root.mainloop()
