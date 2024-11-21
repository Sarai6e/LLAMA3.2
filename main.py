import ollama

prompt = "Escribe un articulo sobre chat gpt"
modelo = "llama3.2"

response = ollama.chat(model=modelo,
                       messages=[
                             {'role': 'user', 'content':prompt}
                             ])
print(response['message']['content'])

