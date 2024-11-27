import cv2
import numpy as np
from PIL import Image
import easyocr
import ollama
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration


def extract_text_from_image(image_path):
    """Extrae texto de una imagen usando EasyOCR."""
    try:
        # Inicializa el lector de EasyOCR (ajusta los idiomas según tu necesidad)
        reader = easyocr.Reader(['es', 'en'])  # Español e inglés
        result = reader.readtext(image_path, detail=0)
        return "\n".join(result)
    except Exception as e:
        raise ValueError(f"Error al procesar la imagen con OCR: {e}")


def analyze_image_visuals(image_path):
    """Genera una descripción detallada de la imagen (contenido visual)."""
    try:
        # Cargar modelo de BLIP para generación de descripciones de imágenes
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

        # Cargar la imagen
        img = Image.open(image_path).convert("RGB")

        # Preprocesar la imagen y generar la descripción
        inputs = processor(images=img, return_tensors="pt")
        out = model.generate(**inputs)
        description = processor.decode(out[0], skip_special_tokens=True)

        return description
    except Exception as e:
        raise ValueError(f"Error al analizar la imagen: {e}")


def get_document_content(file_path):
    """Identifica el tipo de archivo y extrae el contenido."""
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        text_content = extract_text_from_image(file_path)
        visual_analysis = analyze_image_visuals(file_path)
        return f"Texto extraído:\n{text_content}\n\nAnálisis visual:\n{visual_analysis}"
    else:
        raise ValueError("Formato de archivo no soportado. Usa imágenes con extensiones .png, .jpg o .jpeg.")


def ask_about_document(file_path, question, model="llama3.2-vision"):
    """Procesa el contenido del archivo y responde a la pregunta utilizando el modelo."""
    document_content = get_document_content(file_path)
    prompt = f"Documento: {document_content}\n\nPregunta: {question}"
    
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']


# Ejemplo de uso
if __name__ == "__main__":
    file_path = "C:\\Users\\ALUMNO\\Downloads\\machu picchu.jpg"  # Cambia esto por la ruta de tu imagen
    question = "¿Qué contiene la imagen? Describe sus características."
    
    try:
        answer = ask_about_document(file_path, question)
        print("Respuesta:", answer)
    except Exception as e:
        print("Error:", e)
