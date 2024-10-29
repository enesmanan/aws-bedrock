import json
import csv
import boto3
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-west-2",
)

# Read data from a CSV file
def read_products_from_csv(file_path):
    products = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            products.append(row)  
    return products

sentences = read_products_from_csv('e_ticaret_urunleri.csv')


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
    modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
    accept = "application/json"
    contentType = "application/json"
    
    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())
    return response_body['content'][0]['text']

def rag_setup(query):
    global conversation_history
    
    embeddings = BedrockEmbeddings(
        client=bedrock_runtime,
        model_id="amazon.titan-embed-text-v1",
    )
    local_vector_store = FAISS.from_texts(sentences, embeddings)
    docs = local_vector_store.similarity_search(query)
    context = ""
    for doc in docs:
        context += doc.page_content
    
    system_instruction = """Alışgidiş, popüler markalara ve sevilen ürünlere erişim sağlayan, kesintisiz ve güvenli bir alışveriş deneyimi sunan dijital bir alışveriş merkezidir. 
    Sadece "Alışgidiş Limiti" adı verilen benzersiz bir harcama limiti sunmakla kalmaz, aynı zamanda diğer güvenli ve kullanışlı ödeme seçenekleri de sağlar.
    Sen bu mağazanın sanal asistanı FingerBot'sun, senin görevin müşteriye uygun ürünü önermek. 
    Aşağıdaki bağlam bilgisini kullan:
    {context}
    
    Lütfen bu bilgileri kullanarak kullanıcının sorusuna yanıt ver."""
    
    user_message = {
        "role": "user",
        "content": system_instruction + "\n\nKullanıcı Sorusu: " + query
    }
    
    messages = conversation_history + [user_message]
    
    response = call_claude(messages)
    
    conversation_history.append(user_message)
    conversation_history.append({"role": "assistant", "content": response})
    
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]
    
    return response

def chat_loop():
    print("FingerBot: Merhaba! Size nasıl yardımcı olabilirim?")
    while True:
        user_input = input("Siz: ")
        if user_input.lower() in ['çıkış', 'exit', 'quit']:
            print("FingerBot: Görüşmek üzere! İyi günler.")
            break
        response = rag_setup(user_input)
        print("FingerBot:", response)

chat_loop()