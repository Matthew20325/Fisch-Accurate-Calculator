import customtkinter as ctk
import fandom
import requests
from bs4 import BeautifulSoup
from tkinter import messagebox

# Initialize customtkinter theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Table of word-multiplier pairs (modified for new modifiers)
word_multiplier_table = {
    "Sunken": 8.0,        # 700%
    "Aurora": 6.5,        # 550%
    "Mythical": 4.5,      # 350%
    "Atlantean": 3.0,     # 200%
    "Nuclear": 3.0,       # 200%
    "Hexed": 2.0,         # 100%
    "Midas": 2.0,         # 100%
    "Ghastly": 2.0,       # 100%
    "Sinister": 1.9,      # 90%
    "Shiny": 1.85,        # 85%
    "Sparkling": 1.85,    # 85%
    "Electric": 1.6,      # 60%
    "Glossy": 1.6,        # 60%
    "Silver": 1.6,        # 60%
    "Mosaic": 1.5,        # 50%
    "Darkened": 1.3,      # 30%
    "Translucent": 1.3,   # 30%
    "Frozen": 1.3,        # 30%
    "Negative": 1.3,      # 30%
    "Albino": 1.1,        # 10%
    "Big": 1.0,           # 0%
    "Giant": 1.0          # 0%
}

# Function to execute the scraping logic
def scrape_fandom_page():
    # Set the target Fandom wiki to "Fisch"
    fandom.set_wiki("fisch")

    # Get the page name, weight, and modifier word from the input fields
    page_name = page_name_entry.get()
    try:
        weight = float(weight_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for weight.")
        return

    modifier_word = modifier_word_entry.get().strip()  # Get the word from the new text box
    # Capitalize the first letter of the modifier word
    modifier_word = modifier_word.capitalize()

    # Look up the modifier word in the table to get the multiplier
    multiplier = word_multiplier_table.get(modifier_word, 1)  # Default to 1 if no match is found

    # Attempt to retrieve the specified page directly
    try:
        page = fandom.page(page_name)
        
        # Fetch the raw HTML content of the page using requests
        page_url = page.url
        response = requests.get(page_url)
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Now that we have the URL, scrape from the fetched URL
        url_to_scrape = page_url  # Using the URL from the fandom page
        
        # Send a GET request to fetch the webpage content
        response = requests.get(url_to_scrape)

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Try to find the value of C$/Kg first
        price = None
        cskg_element = soup.find(string="C$/Kg")
        if cskg_element:
            price = cskg_element.find_next("td").text.strip()

        # If C$/Kg is not found, look for Lowest Kg
        if not price:
            lowest_kg_element = soup.find(string="Lowest Kg")
            if lowest_kg_element:
                price = lowest_kg_element.find_next("td").text.strip()

        # Process the price and display the result
        if price:
            # Clean up the price string, removing non-numeric characters (like "kg" or "$")
            price_cleaned = ''.join(filter(str.isdigit, price.replace(".", "")))  # Keep only digits and period
            if price_cleaned:
                price = float(price_cleaned)  # Convert to float

                # Calculate total price
                total_price = price * weight * multiplier  # Multiply by the modifier if exists

                # Check if modifier word was entered
                if modifier_word:  # If a modifier was entered
                    result_label.configure(text=f"Total Price for {weight} Kg with modifier '{modifier_word}': ${total_price:.2f}")
                else:  # If no modifier word was entered
                    result_label.configure(text=f"Total Price for {weight} Kg: ${total_price:.2f}")
            else:
                messagebox.showerror("Error", "Price format is not recognized.")
        else:
            messagebox.showerror("Error", "Neither C$/Kg nor Lowest Kg were found on this page.")

    except fandom.error.PageError:
        messagebox.showerror("Page Not Found", f"The page '{page_name}' could not be found on the Fisch fandom.")

# Create the main window
root = ctk.CTk()
root.title("Fish Prices")
root.geometry("400x400")

# Set custom icon (using .ico format)
try:
    root.iconbitmap("icon.ico")  # Replace with your .ico file path
except Exception as e:
    print(f"Error setting icon: {e}")

# Define colors
background_color = "#0a2335"
border_color = "#061724"
text_color = "white"

# Create a main frame to hold all widgets and set background color
main_frame = ctk.CTkFrame(root, fg_color=background_color)
main_frame.pack(fill="both", expand=True, padx=0, pady=0)

# Create and place the input fields and labels with the specified background color
page_name_label = ctk.CTkLabel(main_frame, text="Enter the Fish Name (e.g., 'Pale Tang'):", text_color=text_color)
page_name_label.pack(pady=5)

# Page name entry field with custom border color
page_name_frame = ctk.CTkFrame(main_frame, fg_color=border_color)
page_name_frame.pack(pady=5)
page_name_entry = ctk.CTkEntry(page_name_frame, width=280, fg_color=background_color, text_color=text_color, border_width=0)
page_name_entry.pack(padx=1, pady=1)

weight_label = ctk.CTkLabel(main_frame, text="Enter the weight value:", text_color=text_color)
weight_label.pack(pady=5)

# Weight entry field with custom border color
weight_frame = ctk.CTkFrame(main_frame, fg_color=border_color)
weight_frame.pack(pady=5)
weight_entry = ctk.CTkEntry(weight_frame, width=280, fg_color=background_color, text_color=text_color, border_width=0)
weight_entry.pack(padx=1, pady=1)

modifier_word_label = ctk.CTkLabel(main_frame, text="Enter modifier word (optional):", text_color=text_color)
modifier_word_label.pack(pady=5)

# Modifier word entry field with custom border color
modifier_word_frame = ctk.CTkFrame(main_frame, fg_color=border_color)
modifier_word_frame.pack(pady=5)
modifier_word_entry = ctk.CTkEntry(modifier_word_frame, width=280, fg_color=background_color, text_color=text_color, border_width=0)
modifier_word_entry.pack(padx=1, pady=1)

# Scrape and Calculate button with custom border color
button_frame = ctk.CTkFrame(main_frame, fg_color=border_color)
button_frame.pack(pady=20)
scrape_button = ctk.CTkButton(button_frame, text="Calculate", command=scrape_fandom_page, fg_color=background_color, hover_color=border_color, text_color=text_color, border_width=0)
scrape_button.pack(padx=1, pady=1)

# Label to display the result
result_label = ctk.CTkLabel(main_frame, text="", font=("Arial", 14), text_color=text_color)
result_label.pack(pady=10)

# Start the GUI event loop
root.mainloop()
