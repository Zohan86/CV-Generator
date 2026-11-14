import streamlit as st
import os
from openai import OpenAI
from docx import Document
from docx.shared import Pt

# Настройка страницы
st.set_page_config(page_title="AI Resume Builder", page_icon="🚀", layout="wide")

# Подключение ключа (берем из настроек Streamlit Secrets)
api_key = st.secrets.get("DEEPSEEK_API_KEY")

if not api_key:
    st.error("⚠️ Ошибка: API-ключ DeepSeek не найден в настройках.")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def ask_deepseek(prompt, system_prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка API: {e}"

def create_word_doc(text):
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)
    
    doc.add_heading('РЕЗЮМЕ', 0)
    doc.add_paragraph(text)
    
    doc.save('resume.docx')
    with open('resume.docx', 'rb') as f:
        return f.read()

# --- ИНТЕРФЕЙС ---
st.title("🚀 AI Resume Builder")
st.markdown("Оцените, улучшите и адаптируйте ваше резюме под конкретную вакансию с помощью AI.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Ваше базовое резюме")
    base_resume = st.text_area("Вставьте ваш текст", height=300, placeholder="ФИО, опыт, навыки...")

with col2:
    st.subheader("2. Текст вакансии")
    vacancy_text = st.text_area("Вставьте требования", height=300, placeholder="Требования к кандидату...")

if st.button("🚀 Запустить AI-анализ", type="primary"):
    if not base_resume or not vacancy_text:
        st.warning("Пожалуйста, заполните оба поля!")
    else:
        with st.spinner("Шаг 1: HR-эксперт анализирует резюме..."):
            prompt_1 = f"Оцени это резюме как HRD в IT (1-10). Дай 3-4 совета.\nРезюме:\n{base_resume}"
            expert_feedback = ask_deepseek(prompt_1, "Ты — опытный HR-директор.")
        
        with st.spinner("Шаг 2: Адаптация под вакансию..."):
            prompt_2 = f"Перепиши резюме, используя советы и вакансию.\nРезюме:\n{base_resume}\nСоветы:\n{expert_feedback}\nВакансия:\n{vacancy_text}"
            final_text = ask_deepseek(prompt_2, "Ты — карьерный стратег. Пиши продающим языком.")
        
        with st.spinner("Шаг 3: Генерация Word-файла..."):
            word_file = create_word_doc(final_text)
        
        st.success("✅ Готово!")
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.subheader("Мнение HR-эксперта")
            st.info(expert_feedback)
        with res_col2:
            st.subheader("Финальное резюме")
            st.text_area("Скопируйте текст", value=final_text, height=400)
            st.download_button(
                label="📥 Скачать в Word",
                data=word_file,
                file_name="Improved_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
