import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import datetime
import time
from threading import Thread

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Task management class
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task, priority, reminder_time=None):
        self.tasks.append({"task": task, "priority": priority, "reminder": reminder_time})

    def remove_task(self, task):
        self.tasks = [t for t in self.tasks if t['task'] != task]

    def get_tasks(self):
        return self.tasks

# Initialize task manager
task_manager = TaskManager()

# Voice command function
def listen_for_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("Listening for commands...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        process_command(command)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please try again.")
    except sr.RequestError:
        print("Sorry, I'm having trouble with the speech service. Please try again later.")

# Process voice command
def process_command(command):
    if "add task" in command:
        task = command.replace("add task", "").strip()
        task_manager.add_task(task, "Normal")
        engine.say(f"Task '{task}' added to the list.")
        engine.runAndWait()

    elif "remove task" in command:
        task = command.replace("remove task", "").strip()
        task_manager.remove_task(task)
        engine.say(f"Task '{task}' removed from the list.")
        engine.runAndWait()

    elif "show tasks" in command:
        tasks = task_manager.get_tasks()
        if tasks:
            for task in tasks:
                print(f"Task: {task['task']} | Priority: {task['priority']}")
        else:
            print("No tasks found.")
        engine.say("Showing tasks.")
        engine.runAndWait()

    elif "exit" in command:
        engine.say("Goodbye!")
        engine.runAndWait()
        exit()

# GUI for task manager
def create_gui():
    root = tk.Tk()
    root.title("Voice-Activated Task Manager")

    # Task list display
    task_list_label = tk.Label(root, text="Your Tasks", font=("Arial", 14))
    task_list_label.pack()

    task_listbox = tk.Listbox(root, width=50, height=10)
    task_listbox.pack()

    # Add task button
    def add_task_gui():
        task = task_entry.get()
        if task:
            task_manager.add_task(task, "Normal")
            task_listbox.insert(tk.END, f"{task} - Normal Priority")
            task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    add_button = tk.Button(root, text="Add Task", command=add_task_gui)
    add_button.pack()

    # Task entry field
    task_entry = tk.Entry(root, width=40)
    task_entry.pack()

    # Voice control button
    def start_voice_command():
        Thread(target=listen_for_commands, daemon=True).start()

    voice_button = tk.Button(root, text="Start Voice Command", command=start_voice_command)
    voice_button.pack()

    # Main loop
    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
