from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Respostas automáticas
    if 'quero' in incoming_msg:
        response = "Para ser direcionado para nossos atendentes clique aqui: "
    else:
        response = "Olá! Como posso ajudá-lo? Envie 'menu' para ver nossas opções."

    msg.body(response)
    return str(resp)

if __name__ == '__main__':
    app.run(port=5000)
