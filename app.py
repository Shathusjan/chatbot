from flask import Flask, request, render_template, jsonify, session
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from features.quote import handle_quote_flow
from rag_logic import ask_bot

# Define trigger keywords for starting the quote flow
QUOTE_TRIGGERS = ["get a quote", "quote", "quotation", "pricing", "estimate", "do quote", "help with quote"]

# Load business info once at startup
with open("business_info.json") as f:
    business_info = json.load(f)

# Load environment variables
load_dotenv()

# Init Flask
app = Flask(__name__)

# Init OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Required for using sessions
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret123")

# Route: Home page with chat UI
@app.route('/')
def home():
    return render_template('drift_chatbot.html')

@app.route('/quote', methods=['POST'])
def quote():
    user_input = request.json.get("message", "")
    reply, options = handle_quote_flow(user_input, session)
    return jsonify({
        "reply": reply,
        "options": options or []
    })


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").strip().lower()

    # Reset flow if user greets (fresh start)
    if user_input in ["hi", "hello", "hey"]:
        session["quote_in_progress"] = False
        return jsonify({
            "reply": "👋 Hey there! How can I help you today?",
            "options": []
        })

    # If quote flow is in progress, route all messages there
    if session.get("quote_in_progress"):
        reply, options = handle_quote_flow(user_input, session)
        return jsonify({
            "reply": reply,
            "options": options or []
        })

    # Check for quote trigger (flexible matching)
    if any(trigger in user_input for trigger in QUOTE_TRIGGERS):
        session["quote_in_progress"] = True
        reply, options = handle_quote_flow("start", session)
        return jsonify({
            "reply": reply,
            "options": options or []
        })

    # Otherwise handle normally with rag_logic (small talk / knowledge)
    try:
        from rag_logic import retrieve_context

        try:
            context_chunks = retrieve_context(user_input)
        except Exception:
            context_chunks = []

        if context_chunks:
            system_prompt = (
                "You are Magnolia Cake’s assistant. "
                "Always ground your answers in the following knowledge base:\n\n"
                + "\n".join(context_chunks)
            )
        else:
            system_prompt = (
                "You are Magnolia Cake’s assistant. "
                "Answer the user's questions to the best of your ability."
            )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply,
            "options": []
        })
    except Exception as e:
        print("ERROR", e)
        return jsonify({
            "reply": "Sorry, there was an error.",
            "options": []
        })

# Run
if __name__ == '__main__':
    app.run(debug=True)