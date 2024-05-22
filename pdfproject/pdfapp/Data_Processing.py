import pymupdf
import google.generativeai as genai
import markdown
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Access API key
API_KEY = os.getenv('API_KEY')

# pdf_folder = "C:/Users/Hp/Documents/Organized Folders/Project Files/PDF Text Extractor/Pdf" 
pdf_folder = "pdfapp/Pdf" 

genai.configure(api_key=API_KEY)
generation_config = {
"temperature": 1,
"top_p": 0.95,
"top_k": 64,
"max_output_tokens": 8192,
"response_mime_type": "text/plain",
}
safety_settings = [
{
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
},
{
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
},
{
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
},
{
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
},
]

model = genai.GenerativeModel(
model_name="gemini-1.5-flash-latest",
safety_settings=safety_settings,
generation_config=generation_config,
)

chat_session = model.start_chat(
    history=[
    ]
    )








def file_hunt():
    # pdf_folder1 = "C:/Users/Hp/Documents/Organized Folders/Project Files/PDF Text Extractor/Pdf/2024_April" 
    # pdf_folder2 = "C:/Users/Hp/Documents/Organized Folders/Project Files/PDF Text Extractor/Pdf/2024_Jan"

    pdf_paths = []

    filenames = []

    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            # Construct the path to the PDF file
            filenames.append(filename)
            pdf_path = os.path.join(pdf_folder, filename)
            # print(pdf_path)
            # print(filename[29:44])
            pdf_paths.append(pdf_path)

    # for filename in os.listdir(pdf_folder2):
    #     if filename.endswith(".pdf"):
    #         # Construct the path to the PDF file
    #         filenames.append(filename)
    #         # print(filename[29:44])
    #         pdf_path = os.path.join(pdf_folder2, filename)
    #         # print(pdf_path)
    #         pdf_paths.append(pdf_path)


    pdf_data = []

    for path in pdf_paths:
        doc = pymupdf.open(f"{path}")
        pdf_contents = []
        for page in doc: 
            text = page.get_text()
            pdf_contents.append(text)
        pdf_data.append(pdf_contents)
    # return pdf_data
    return filenames

def ai_response(path):

    pdf_path = os.path.join(pdf_folder, path)
    print(f"Path found: {path}")
    print("success in first attempt")
    doc = pymupdf.open(f"{pdf_path}")
    pdf_contents = []
    for page in doc: 
        text = page.get_text()
        pdf_contents.append(text)


   
    
    # response = chat_session.send_message(f"You are a Data Analyst. You are given raw data of JEE mains question papers {text}. Your job is to generate insights from this data and return it.")
    
    response = chat_session.send_message(f"You are a Data Analyst. You are given this data: {pdf_contents}. Your job is to answer any queries user may have regarding this data. Say hello!")

    print('chat response text')
    # print(response.text[:100])
    # print('chat response text end')
    print()
    print()
    print()
    print()
    print()
    print(chat_session.history)
    print()
    print()
    print()
    print()

    return response.text

def stream_chat(prompt):
    chat_response = chat_session.send_message(prompt)
    print(chat_session.history)
    return chat_response.text