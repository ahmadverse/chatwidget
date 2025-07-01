from flask import Flask, request, jsonify, render_template
from groq import Groq
import os

app = Flask(__name__)

def generate_response(user_query):
    client = Groq(api_key="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")
    
    # Enhanced system prompt for better formatting
    system_prompt = """You are Ahmad GPT, a helpful AI assistant. Please format your responses clearly:

- Use **bold** for important points
- Use *italics* for emphasis
- Use `code blocks` for technical terms or code
- Use line breaks to separate paragraphs
- Use numbered lists (1. 2. 3.) for step-by-step instructions
- Use bullet points (- or •) for lists
- Keep responses well-structured and easy to read

Always be helpful, clear, and concise in your responses."""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_query,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.7,  # Slightly higher for more creative formatting
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )
    
    response_text = chat_completion.choices[0].message.content
    
    # Clean up the response text
    response_text = response_text.strip()
    
    return response_text

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        data = request.get_json()
        user_query = data.get('query', '')
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400
        
        # Generate AI response
        ai_response = generate_response(user_query)
        
        return jsonify({"response": ai_response})
    
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return jsonify({"response": "Sorry, I encountered an error. Please try again later."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860, debug=True)