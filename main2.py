import ollama
import easyocr

def extract_text_from_image(image_path):
    """Extrae texto de una imagen usando EasyOCR."""
    try:
        # Inicializa el lector de EasyOCR (ajusta los idiomas según tu necesidad)
        reader = easyocr.Reader(['es', 'en'])  # Español y/o inglés
        result = reader.readtext(image_path, detail=0)
        return "\n".join(result)
    except Exception as e:
        raise ValueError(f"Error al procesar la imagen con OCR: {e}")

def get_document_content(file_path):
    """Identifica el tipo de archivo y extrae el contenido."""
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        return extract_text_from_image(file_path)
    else:
        raise ValueError("Formato de archivo no soportado. Usa imágenes con extensiones .png, .jpg o .jpeg.")

def ask_about_document(file_path, question, model="llama3.2"):
    """Procesa el contenido del archivo y responde a la pregunta utilizando el modelo."""
    document_content = get_document_content(file_path)
    prompt = f"Documento: {document_content}\n\nPregunta: {question}"
    
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

# Ejemplo de uso:
file_path = "C:\\Users\\ALUMNO\\Downloads\\gpt.png"  # Cambia esto por la ruta de tu imagen
question = "¿Describeme lo que contiene?"

try:
    answer = ask_about_document(file_path, question)
    print("Respuesta:", answer)
except Exception as e:
    print("Error:", e)
