import json
import boto3

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2",
)

conversation_history = []

def call_claude(messages):
    prompt_config = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": messages,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 0.5,
    }
    body = json.dumps(prompt_config)
    #modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
    modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    accept = "application/json"
    contentType = "application/json"
    
    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())
    return response_body['content'][0]['text']

def process_query(query):
    global conversation_history
    
    system_instruction = """Alışgidiş, popüler markalara ve sevilen ürünlere erişim sağlayan, kesintisiz ve güvenli bir alışveriş deneyimi sunan dijital bir alışveriş merkezidir. 
    Sadece "Alışgidiş Limiti" adı verilen benzersiz bir harcama limiti sunmakla kalmaz, aynı zamanda diğer güvenli ve kullanışlı ödeme seçenekleri de sağlar.
    Sen bu mağazanın sanal asistanı FingerBot'sun, senin görevin müşteriye yardımcı olmak ve sorularını yanıtlamak. 

    """

    if not conversation_history:
        user_message = {
            "role": "user",
            "content": system_instruction + "\n\nKullanıcı: " + query
        }
    else:
        user_message = {
            "role": "user",
            "content": query
        }
    
    # Construct messages array with history
    messages = conversation_history + [user_message]
    
    # Get response from Claude
    response = call_claude(messages)
    
    # Update conversation history
    conversation_history.append(user_message)
    conversation_history.append({"role": "assistant", "content": response})
    
    # Keep only the last 10 messages to avoid token limit issues
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]
    
    return response

def chat_loop():
    print("FingerBot: Merhaba, Selim! Ben alışgidiş dehası FingerBot, en iyi ürünleri sizin için bulmaya hazırım. Başlayalım mı?")
    while True:
        user_input = input("Siz: ")
        if user_input.lower() in ['çıkış', 'exit', 'quit']:
            print("FingerBot: Görüşmek üzere! İyi günler.")
            break
        response = process_query(user_input)
        print("FingerBot:", response)

chat_loop()