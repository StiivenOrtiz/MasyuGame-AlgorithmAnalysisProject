import tkinter as tk
from tkinter import filedialog
import os

def select_file():
    # Create a Tkinter root window with no GUI elements
    root = tk.Tk()
    root.withdraw()  # Ocult the root window

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Explore the project root
    project_root = os.path.abspath(os.path.join(script_dir, os.pardir, os.pardir))
    
    # Construct the initial directory
    initial_dir = os.path.join(project_root, "games")

    # Verify if the directory exists
    if not os.path.exists(initial_dir):
        print(f"La carpeta {initial_dir} no existe.")
        return None

    # Open a file dialog
    file_path = filedialog.askopenfilename(initialdir=initial_dir, title="Selecciona un archivo",
                                           filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")))
    return file_path