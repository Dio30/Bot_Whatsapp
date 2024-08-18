from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Substitua pelo seu Access Token da API do WhatsApp
access_token = 'EAAV12WyY078BO6ZBEl09S35ZBiaOAcZAZAZAVeYpy58lpgwcCJ7FnURfRGS40SOcIYsoIoKYYABduE5VWtK1cVCUdqdZCbo7dSp37lmzFled7pfZBhHl2ZAogkEd8aZC8u9NhI1i7BPjKI3vtvl2vYZAmjcGZASN3g5fiZC3VZCtr120gcQLHvkZCYabtguAxRL1PBZBvfJYzISxggZB9VsOZC7D08mMZD'

# Substitua pelo seu ID de telefone do WhatsApp Business
phone_number_id = '405104159346148'

# URL para a API do WhatsApp
whatsapp_api_url = f'https://graph.facebook.com/v20.0/{phone_number_id}/messages'

# Cabeçalhos da requisição HTTP
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

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
        
        # Verifique se recebemos uma mensagem
        if 'messages' in data['entry'][0]['changes'][0]['value']:
            # Dados da mensagem recebida
            messages = data['entry'][0]['changes'][0]['value']['messages'][0]
            message_text = messages['text']['body'] if 'text' in messages else None
            sender_id = '+5548998098694' # O número do telefone do remetente
            
            # Lógica de resposta
            if message_text:
                reply_text = f"Você disse: {message_text}"
                send_message(sender_id, reply_text)
        
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

if __name__ == '__main__':
    # O webhook será exposto no localhost na porta 5000
    app.run(port=5000)
