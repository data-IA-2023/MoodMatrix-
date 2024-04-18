from flask import Flask, render_template, request
import datetime

from main import text_analyse_et_generation, get_df_bd_monitoring, get_df_bd_historique

app = Flask(__name__)

chat_history = []

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        user_input = request.form['user_input']
        if user_input:
            
            idConversation = len(chat_history) + 1  # Generate a unique conversation ID
            dateHistorique = datetime.datetime.now()
            result = text_analyse_et_generation(user_input, idConversation, dateHistorique)
            bot_response = result['resultat']
            bot_emotion = result['sentiment']
            bot_emoticon = result['emoticon']
            
            # Append user input and bot response to chat history with timestamp
            chat_history.append({"user": user_input, "emotion": bot_emotion, "emoticon": bot_emoticon, "sender": "user", "time": dateHistorique.strftime("%H:%M")})
            chat_history.append({"user": bot_response, "emotion": bot_emotion, "emoticon": bot_emoticon, "sender": "bot", "time": dateHistorique.strftime("%H:%M")})
            
    return render_template('index.html', chat_history=chat_history)

@app.route('/refresh', methods=['GET', 'POST'])
def refresh():
    chat_history.clear()  # Clear the chat history
    return render_template('index.html', chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
