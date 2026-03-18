import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Табель ЗП: Денис и Анна", page_icon="📅")

# --- НАСТРОЙКИ ---
RATE = 10320
TAX = 0.05

st.title("📅 Табель зарплаты")

# Создаем простую базу данных в памяти сессии (пока без внешних файлов)
if 'journal' not in st.session_state:
    st.session_state.journal = pd.DataFrame(columns=["Дата", "Имя", "Тип", "Чаноб", "Итого (чистыми)"])

# --- ФОРМА ВВОДА ---
with st.form("work_day"):
    st.write("### Добавить смену")
    date = st.date_input("Дата", datetime.now())
    user = st.radio("Кто работал?", ["Денис", "Анна"], horizontal=True)
    day_type = st.selectbox("Тип дня", ["Будни (8ч + чаноб)", "Выходной (только часы)"])
    overtime = st.number_input("Часы (х1.5)", min_value=0.0, step=0.5)
    
    submit = st.form_submit_button("СОХРАНИТЬ В ТАБЛИЦУ")

if submit:
    # Расчет
    if "Будни" in day_type:
        before_tax = (8 * RATE) + (overtime * RATE * 1.5)
    else:
        before_tax = (overtime * RATE * 1.5)
    
    total = before_tax * (1 - TAX)
    
    # Добавление в таблицу
    new_row = pd.DataFrame({
        "Дата": [date.strftime("%d.%m")],
        "Имя": [user],
        "Тип": [day_type],
        "Чаноб": [overtime],
        "Итого (чистыми)": [round(total)]
    })
    st.session_state.journal = pd.concat([st.session_state.journal, new_row], ignore_index=True)
    st.success(f"Записано для {user}!")

# --- ТАБЛИЦА И ИТОГИ ---
st.write("---")
st.write("### Журнал за месяц")
st.dataframe(st.session_state.journal, use_container_width=True)

# Считаем общие итоги
if not st.session_state.journal.empty:
    total_denis = st.session_state.journal[st.session_state.journal['Имя'] == 'Денис']['Итого (чистыми)'].sum()
    total_anna = st.session_state.journal[st.session_state.journal['Имя'] == 'Анна']['Итого (чистыми)'].sum()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Денис всего:", f"{total_denis:,.0f} ₩")
    with col2:
        st.metric("Анна всего:", f"{total_anna:,.0f} ₩")
    
    st.divider()
    st.subheader(f"ОБЩИЙ БЮДЖЕТ: {(total_denis + total_anna):,.0f} вон")
