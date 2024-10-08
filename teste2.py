from flask import Flask, request, jsonify, render_template, flash
import requests
import json

app = Flask(__name__)
app.secret_key = 'teste1234'

# Substitua pelo seu Access Token da API do WhatsApp
access_token = 'EAAV12WyY078BO0UxQdZCeyFXruZBBo7Ny6TBNWZBtyktAcdpDzmKjGcZCfym0KZCG7N0ra2rZBUg7D1kPB9ER45PIutJmV7EHhqYZBOo539sWGB5CuicrsJXKQaeFW5uZCZBaEbxQCl8cDCZCpdtkpTf2qzZCmQ8RUm3drtCfyCx4Ik45URb8exPRLNwn2YsfG4SMjxXQZDZD'

# Substitua pelo seu ID de telefone do WhatsApp Business
phone_number_id = '413045388554931'

# URL para a API do WhatsApp
whatsapp_api_url = f'https://graph.facebook.com/v20.0/{phone_number_id}/messages'
templates_api_url = f'https://graph.facebook.com/v20.0/{phone_number_id}/message_templates'

# Cabeçalhos da requisição HTTP
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

received_messages = []

def adicionar_digito_nove(numero):
    # Verifica se o número tem 10 dígitos (formato DDD + número de 8 dígitos)
    if numero.startswith("55") and len(numero) == 12:  # Com código do país (55)
        numero = numero[:4] + "9" + numero[4:]  # Adiciona o 9 após o DDD
    elif len(numero) == 10:  # Sem código do país
        numero = numero[:2] + "9" + numero[2:]  # Adiciona o 9 após o DDD
    
    numero = "+55489" + numero
    
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
        print(data)
        
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
                received_messages.append({
                    'sender_id': sender_id,
                    'user_name': user_name,
                    'message_text': message_text
                    })
                
                print("Mensagens armazenadas:", received_messages)

                if message_text == "sim":
                    sender_id_com_nove = adicionar_digito_nove(sender_id)
                    reply_text = f"{user_name}, você pode falar com nossos atendentes através desse link: https://wa.me/554898098694"

                elif message_text in ["nao", "não"]:
                    sender_id_com_nove = adicionar_digito_nove(sender_id)
                    reply_text = f"Obrigado pelo retorno {user_name}, caso mude de ideia informe com um sim"

                else:
                    sender_id_com_nove = adicionar_digito_nove(sender_id)
                    reply_text = "Só entendo respostas como sim ou não."
                    
                send_message(sender_id_com_nove, reply_text) # mensagem de retorno a mensagem do cliente

        return jsonify({'status': 'success'}), 200
            
def send_message(recipient_phone_number, message_text=None, template_name=None):
    if template_name:
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": "pt_BR"  # Código de linguagem para Português Brasileiro
                },
            }
        }
    else:
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_phone_number,
            "type": "text",
            "text": {
                "body": message_text
            }
        }
    
    response = requests.post(whatsapp_api_url, headers=headers, data=json.dumps(payload))
    return response.json()

@app.route('/enviar_mensagem', methods=['POST'])
def send_custom_message():
    phone_number = request.form.get('phone_number')
    template_name = 'iniciar_conversa'
    response_status = []

    if phone_number and template_name:
        phone_numbers_list = [numero.strip() for numero in phone_number.split(',')]

        for phone_number in phone_numbers_list:
            response = send_message(phone_number, template_name=template_name)
            if response.get('error'):
                response_status.append(f'Falha ao enviar para {phone_number}: {response["error"]["message"]}')
            else:
                response_status.append(f'Mensagem enviada com sucesso para {phone_number}!')
        
        for status in response_status:
            flash(status, 'success' if 'sucesso' in status else 'danger')
    
    else:
        flash('Números de telefone ou template ausente!', 'warning')
        
    return render_template('index.html')

@app.route('/')
def home():
    return render_template('index.html', received_messages=received_messages)

if __name__ == '__main__':
    app.run(port=5000)