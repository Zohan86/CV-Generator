# generate_resume.py
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_resume():
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    # Заголовок
    title = doc.add_heading('Савельев Алексей Анатольевич', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('Senior IT Project Manager / Руководитель проектов (PMP)')
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x2F, 0x54, 0x96)

    contacts = doc.add_paragraph()
    contacts.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contacts.add_run('Москва | +7 (916) 986-26-79 | alexeysav86@gmail.com | Telegram: @alexey_savelev_86').font.size = Pt(10)

    # О себе
    doc.add_heading('КРАТКО О ПРОФЕССИОНАЛЬНОМ ОПЫТЕ', level=1)
    p = doc.add_paragraph()
    p.add_run('17 лет опыта в IT и Hardware. Специализируюсь на выводе сложных IT-продуктов (MES, ERP, SRM) и физических устройств из состояния «идеи» в «промышленную эксплуатацию» в срок и в рамках бюджета.\n\n')
    p.add_run('• Управление: ').bold = True
    p.add_run('Бюджеты до 200 млн руб., команды до 25+ человек.\n')
    p.add_run('• Технологии: ').bold = True
    p.add_run('PMP, SAFe Agilist. Инженерное образование (мехатроника).\n')
    p.add_run('• Инновации: ').bold = True
    p.add_run('Магистр ВШЭ по ИИ. Внедрение ML-моделей в бизнес-процессы.')

    # Опыт работы
    doc.add_heading('ОПЫТ РАБОТЫ', level=1)

    def add_job(company, dates, role, bullets):
        p = doc.add_paragraph()
        p.add_run(f'{company} | {dates}\n').bold = True
        p.add_run(f'{role}\n').italic = True
        for b in bullets:
            p.add_run(f'• {b}\n')
        doc.add_paragraph()

    add_job('МТС (Телеком/IT)', 'Июль 2024 — Настоящее время', 'Руководитель проектов / Владелец продукта',
            ['Цифровая трансформация закупок.', 'Бюджет 200 млн руб., команда 25+ чел.', 'Сокращение времени согласований на 30%.'])
    
    add_job('YADRO (IT-производитель)', 'Июнь 2023 — Июль 2024', 'Руководитель ИТ-проектов',
            ['Внедрение систем управления закупками.', 'Запуск на 1,5 месяца раньше плана.', 'Сокращение расходов на 20%.'])
    
    add_job('Rockwell Automation', 'Февраль 2018 — Декабрь 2022', 'Менеджер проектов (MES)',
            ['Внедрение MES на заводе грузовиков.', 'Управление Pre-sale и техподдержкой SLA.'])
    
    add_job('AKKA Technologies', 'Август 2014 — Февраль 2018', 'Менеджер проектов (Hardware)',
            ['Lada X-Ray: запуск 100 деталей, экономия 12%.', 'Toyota: запуск электроники, рост выручки 15%.'])

    add_job('Ранний опыт', '2008 — 2014', 'Инженер / Менеджер',
            ['Nissan: запуск 2 моделей.', 'Sungwoo Hitech: создание отдела с нуля.', 'ВИРА/ПетроКРАН: инженер-конструктор.'])

    # Образование
    doc.add_heading('ОБРАЗОВАНИЕ И КВАЛИФИКАЦИЯ', level=1)
    doc.add_paragraph('• 2026: НИУ ВШЭ — Магистр, «Управление инновационным предприятием» (ИИ).\n• 2008: БГТУ «ВОЕНМЕХ» — Инженер, «Мехатроника и робототехника».\n• Сертификаты: PMP (PMI), SAFe 6 Agilist.')

    # Навыки
    doc.add_heading('КЛЮЧЕВЫЕ НАВЫКИ', level=1)
    doc.add_paragraph('• Методологии: PMBOK, Agile, Scrum, Waterfall, SAFe.\n• Инструменты: Jira, MS Project, Confluence, 1C.\n• Языки: Русский, Английский (C1), Французский (B2).')

    doc.save('Savelyev_Resume.docx')

if __name__ == '__main__':
    create_resume()
