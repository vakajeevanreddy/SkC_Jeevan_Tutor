from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        # Get API key from request headers
        api_key = request.headers.get('X-API-Key')
        if api_key:
            openai.api_key = api_key
            
        if not openai.api_key:
            return jsonify({'error': 'API key not configured'}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly and patient Python programming tutor for children. Explain concepts in simple terms, use analogies, and encourage learning through examples."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return jsonify({
            'response': response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)
