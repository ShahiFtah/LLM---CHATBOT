from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # Tillater forespørsler fra frontend

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="PASTE YOUR API",
)

def format_bot_reply(reply):
    # Denne funksjonen kan formatere AI-svaret for bedre struktur
    reply = reply.replace("\n", "<br>")  # Legg til linjeskift for bedre lesbarhet
    return f"<p>{reply}</p>"  # Omgi svaret med <p> for å lage avsnitt

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Melding mangler!"}), 400

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3.3-8b-instruct:free",
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response.choices[0].message.content if response.choices else "⚠ Ingen svar fra AI-en."
        
        # Formatere svaret fra boten
        formatted_reply = format_bot_reply(bot_reply)

        return jsonify({"reply": formatted_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":

    app.run(debug=True)
