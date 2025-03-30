import tkinter as tk
from tkinter import messagebox

last_alert = None  # Keeps track of the last alert message to avoid duplicates

class ShowAlert:
    @staticmethod
    def show(title, message):
        global last_alert
        if last_alert == message:
            return  # Prevent showing the same alert multiple times
        last_alert = message  # Update the last alert message
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window since we only need the alert
        messagebox.showwarning(title, message)  # Display the warning message
        root.destroy()  # Close the hidden Tkinter window
