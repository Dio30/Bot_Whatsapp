from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# Substitua pelo seu Access Token da API do WhatsApp
access_token = 'EAAV12WyY078BOzvmpQy3fRYsNyKf0LbqYIgKgoebP4ZAOS1ZBjJqrZB2fM6xxo3DTc1kaiOd0NZCg7JiiRTfNqnldH67f1CxFcIfM1dr0To8EsqBVrL8fOokXrtnoQvjh4bbiBBpZBJZC8ZBeYohlbW8DWQmV26mlt4ZACerMVrFWUDqcKxEFOYiSq3claNSQ4ZAmVKIu6ZChwBboZCL84l6hKX'

# Substitua pelo seu ID de telefone do WhatsApp Business
phone_number_id = '413045388554931'

# URL para a API do WhatsApp
whatsapp_api_url = f'https://graph.facebook.com/v20.0/{phone_number_id}/messages'

# Cabeçalhos da requisição HTTP
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

def adicionar_digito_nove(numero):
    # Verifica se o número tem 10 dígitos (formato DDD + número de 8 dígitos)
    if numero.startswith("55") and len(numero) == 12:  # Com código do país (55)
        numero = numero[:4] + "9" + numero[4:]  # Adiciona o 9 após o DDD
    elif len(numero) == 10:  # Sem código do país
        numero = numero[:2] + "9" + numero[2:]  # Adiciona o 9 após o DDD
    
    return numero

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = 'dione1234'
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == verify_token:
            return challenge, 200
        else:
            return 'Verificação falhou', 403
    
    if request.method == 'POST':
        data = request.get_json()
        print(json.dumps(data))
        
        # Verifique se recebemos uma mensagem
        if 'messages' in data['entry'][0]['changes'][0]['value']:
            # Dados da mensagem recebida
            messages = data['entry'][0]['changes'][0]['value']['messages'][0]
            message_text = messages['text']['body'].lower() if 'text' in messages else None # trazer texto se não None
            sender_id = messages['from']  # O número do telefone do remetente
            contacts = data['entry'][0]['changes'][0]['value'].get('contacts', [])
            user_name = contacts[0]['profile']['name'] if contacts else "Futuro Cliente"

            # Lógica de resposta com condicional
            if message_text:
                if "sim" in message_text:
                    sender_id_com_nove = adicionar_digito_nove(sender_id)
                    reply_text = f"{user_name}, você pode falar com nossos atendentes através desse link: https://wa.me/554898098694"
                    print(reply_text)

                elif "nao" or "não" in message_text:
                    sender_id_com_nove = adicionar_digito_nove(sender_id)
                    reply_text = f"Obrigado pelo retorno {user_name}, caso mude de ideia informe com um sim"
                    print(reply_text)
                    
                else:
                    sender_id_com_nove = adicionar_digito_nove(sender_id)
                    reply_text = "Responda com sim ou não por favor"
                    print(reply_text)

                send_message(sender_id_com_nove, reply_text)
        return jsonify({'status': 'success'}), 200
            
def send_message(recipient_phone_number, message_text):
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient_phone_number,
        "type": "text",
        "text": {
            "body": message_text
        }
    }
    
    response = requests.post(whatsapp_api_url, headers=headers, data=json.dumps(payload))
    
    # Exibindo a resposta da API
    print(response.status_code)
    print(response.json())

@app.route('/')
def home():
    return render_template('index.html', status=None)

@app.route('/enviar_mensagem', methods=['POST'])
def send_custom_message():
    phone_number = request.form.get('phone_number')
    message_text = request.form.get('message')
    status = None

    if phone_number and message_text:
        status_code = send_message(phone_number, message_text)
        
        if status_code == 200:
            status = 'Mensagem enviada com sucesso!'
      
        return render_template('index.html', context={'status':status})
    else:
        status = 'Número de telefone ou mensagem ausente!'
        
    return render_template('index.html', context={'status':status})

if __name__ == '__main__':
    # O webhook será exposto no localhost na porta 5000
    app.run(port=5000)
