from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "http://localhost:3000"}})

# Simple intent matching
def get_intent(message):
    message = message.lower()
    if any(keyword in message for keyword in ['course', 'courses', 'subject']):
        return 'course'
    elif any(keyword in message for keyword in ['deadline', 'due', 'assignment']):
        return 'deadline'
    return None

# Database query functions
def get_courses():
    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, description FROM courses')
    courses = cursor.fetchall()
    conn.close()
    return courses

def get_deadlines():
    conn = sqlite3.connect('college.db')
    cursor = conn.cursor()
    cursor.execute('SELECT assignment, due_date FROM deadlines')
    deadlines = cursor.fetchall()
    conn.close()
    return deadlines

@app.route('/')
def home():
    return "Backend is running!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message')
        if not user_message:
            return jsonify({'response': 'Bot: No message provided.'}), 400
        
        intent = get_intent(user_message)
        
        if intent == 'course':
            courses = get_courses()
            if courses:
                response = "Bot: Available courses:\n" + "\n".join([f"- {name}: {desc}" for name, desc in courses])
            else:
                response = "Bot: No courses found."
        elif intent == 'deadline':
            deadlines = get_deadlines()
            if deadlines:
                response = "Bot: Deadlines:\n" + "\n".join([f"- {assignment}: Due on {due_date}" for assignment, due_date in deadlines])
            else:
                response = "Bot: No deadlines found."
        else:
            response = f"Bot: You asked: {user_message}. Try asking about courses or deadlines!"
        
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f'Bot: Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)