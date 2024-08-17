import requests
import json

# Substitua pelo seu Access Token da API do WhatsApp
access_token = 'EAAV12WyY078BO5qegE1ALOp6oFtYoaDYang9PmdZArk2nvysGT611nC5Kv91ooo2lTGgZA9rPuUZCSzt215jSdBNeLbaEa8MPccYakcj4i56AA0MCbnqDOetzR2ZCBnajBgW6pZCPMN88HVLruRPshshrxZBJXksIcEXm7ilZCOSWhcBwXtQWqsiTSZApScsb1N3RCpzZBCyfki84jhn7dN4ZD'

# Substitua pelo seu ID de telefone do WhatsApp Business
phone_number_id = '405104159346148'

# Número do destinatário no formato internacional
recipient_phone_number = '+554898098694'

# URL para a API do WhatsApp
url = f'https://graph.facebook.com/v16.0/{phone_number_id}/messages'

# Cabeçalhos da requisição HTTP
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Corpo da requisição com o conteúdo da mensagem
payload = {
    "messaging_product": "whatsapp",
    "to": recipient_phone_number,
    "type": "text",
    "text": {
        "body": "Olá! Esta é uma mensagem automática enviada pelo meu chatbot."
    }
}

# Enviando a mensagem
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Exibindo a resposta da API
print(response.status_code)
print(response.json())
