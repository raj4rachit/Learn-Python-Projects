import PyPDF2
import pyttsx3
import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Global flag to control the speech thread
is_speaking = False

# Functions to control the speech
def start_speech():
    global is_speaking
    if not is_speaking:
        is_speaking = True
        speech_thread = threading.Thread(target=speak_text)
        speech_thread.start()

def speak_text():
    global is_speaking
    text = text_area.get("1.0", tk.END)
    engine.say(text)
    engine.runAndWait()
    is_speaking = False

def stop_speech():
    global is_speaking
    if is_speaking:
        engine.stop()
        is_speaking = False

def pause_speech():
    engine.pause()

def resume_speech():
    engine.resume()

# Function to open and display the PDF content
def open_pdf():
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'rb') as file:
            pdfReader = PyPDF2.PdfReader(file)
            page = pdfReader.pages[1]
            text = page.extract_text()
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.INSERT, text)

# Creating the main window
root = tk.Tk()
root.title("PDF Reader and Text-to-Speech")

# Creating a text area to display PDF content
text_area = scrolledtext.ScrolledText(root, width=60, height=20)
text_area.pack(padx=10, pady=10)

# Creating control buttons
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

open_button = tk.Button(frame, text="Open PDF", command=open_pdf)
open_button.grid(row=0, column=0, padx=5)

start_button = tk.Button(frame, text="Start", command=start_speech)
start_button.grid(row=0, column=1, padx=5)

stop_button = tk.Button(frame, text="Stop", command=stop_speech)
stop_button.grid(row=0, column=2, padx=5)

pause_button = tk.Button(frame, text="Pause", command=pause_speech)
pause_button.grid(row=0, column=3, padx=5)

resume_button = tk.Button(frame, text="Resume", command=resume_speech)
resume_button.grid(row=0, column=4, padx=5)

# Running the Tkinter event loop
root.mainloop()
