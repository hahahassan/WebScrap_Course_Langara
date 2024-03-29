import tkinter as tk
from tkinter import filedialog

from scraper.scraper import scrape_html_to_xlsx  # Import the separate scraping function

def select_html_file():
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if file_path:
        file_path_label.config(text=file_path)
        scrape_button.config(state="normal")

def scrape_and_save():
    html_file_path = file_path_label.cget("text")
    csv_file_path = 'output.csv'  # Define the CSV file path
    scrape_html_to_xlsx(html_file_path, csv_file_path)  # Use the imported function
    status_label.config(text="CSV file has been saved as 'output.csv'.")

# GUI setup remains the same as before
root = tk.Tk()
root.title("HTML to CSV Converter")

select_button = tk.Button(root, text="Select HTML File", command=select_html_file)
select_button.pack(pady=10)

file_path_label = tk.Label(root, text="No file selected", fg="grey")
file_path_label.pack(pady=5)

scrape_button = tk.Button(root, text="Scrape and Save to excel", state="disabled", command=scrape_and_save)
scrape_button.pack(pady=10)

status_label = tk.Label(root, text="", fg="green")
status_label.pack(pady=5)

root.mainloop()