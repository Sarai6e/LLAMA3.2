import ollama
import PyPDF2
from docx import Document

def extract_text_from_pdf(pdf_path):
    """Extrae texto de un archivo PDF."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_word(word_path):
    """Extrae texto de un archivo Word (.docx)."""
    doc = Document(word_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def get_document_content(file_path):
    """Identifica el tipo de archivo y extrae el contenido."""
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_word(file_path)
    else:
        raise ValueError("Formato de archivo no soportado. Usa .pdf o .docx.")

def ask_about_document(file_path, question, model="llama3.2"):
    """Procesa el documento y responde a la pregunta utilizando el modelo."""
    document_content = get_document_content(file_path)
    prompt = f"Documento: {document_content}\n\nPregunta: {question}"
    
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

# Ejemplo de uso:
file_path = "C:\\Users\\SOPORTE\\Downloads\\Agatha Christie - Nido de avispas.pdf"  # Cambia esto por la ruta de tu archivo .pdf o .docx
question = "¿Cuál es el tema principal del documento?"

try:
    answer = ask_about_document(file_path, question)
    print("Respuesta:", answer)
except Exception as e:
    print("Error:", e)






