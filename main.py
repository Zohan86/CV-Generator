from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from openai import OpenAI
from docx import Document
from docx.shared import Pt

app = FastAPI()

# Подключение DeepSeek
api_key = os.environ.get("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

class ProcessRequest(BaseModel):
    resume: str
    vacancy: str

class DownloadRequest(BaseModel):
    text: str

def ask_deepseek(prompt, system_prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
    )
    return response.choices[0].message.content

# Отдаем HTML файл на главной странице
@app.get("/")
def read_root():
    return FileResponse("index.html")

# Эндпоинт для обработки текста нейросетью
@app.post("/api/process")
def process_resume(req: ProcessRequest):
    prompt_1 = f"Оцени это резюме как HRD в IT (1-10). Дай 3-4 совета.\nРезюме:\n{req.resume}"
    feedback = ask_deepseek(prompt_1, "Ты — опытный HR-директор.")

    prompt_2 = f"Перепиши резюме, используя советы и вакансию.\nРезюме:\n{req.resume}\nСоветы:\n{feedback}\nВакансия:\n{req.vacancy}"
    final_resume = ask_deepseek(prompt_2, "Ты — карьерный стратег.")

    return {"feedback": feedback, "final_resume": final_resume}

# Эндпоинт для генерации Word-файла
@app.post("/api/download")
def download_word(req: DownloadRequest):
    doc = Document()
    doc.add_heading('РЕЗЮМЕ', 0)
    
    for paragraph in req.text.split('\n'):
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())
            
    doc.save("temp_resume.docx")
    
    return FileResponse(
        "temp_resume.docx", 
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="Resume.docx"
    )
