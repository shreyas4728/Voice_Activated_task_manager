from flask import Flask, render_template, request
import pyttsx3

app = Flask(__name__)

# Initialize text-to-speech engine
engine = pyttsx3.init()

# In-memory task storage
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if task:
        tasks.append({"task": task, "priority": "Normal"})
        engine.say(f"Task '{task}' added to the list.")
        engine.runAndWait()
    return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
