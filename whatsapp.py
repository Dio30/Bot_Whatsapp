from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Respostas automáticas
    if 'menu' in incoming_msg:
        response = "Nosso menu:\n1. Hambúrguer\n2. Pizza\n3. Salada\n4. Bebidas"
    elif 1 in incoming_msg:
        response = "Temos os seguintes hambúrgueres:\n- Cheeseburger\n- Hambúrguer Duplo\n- Hambúrguer de Frango"
    elif 2 in incoming_msg:
        response = "Temos os seguintes sabores de pizza:\n- Margherita\n- Pepperoni\n- Quatro Queijos"
    elif 3 in incoming_msg:
        response = "Temos as seguintes saladas:\n- Salada Caesar\n- Salada Grega\n- Salada de Frutas"
    elif 4 in incoming_msg:
        response = "Temos as seguintes bebidas:\n- Refrigerante\n- Suco\n- Água"
    else:
        response = "Olá! Como posso ajudá-lo? Envie 'menu' para ver nossas opções."

    msg.body(response)
    return str(resp)

if __name__ == '__main__':
    app.run(port=5000)
