import streamlit as st

st.set_page_config(page_title="Зарплата Денис и Анна", page_icon="💰")
st.title("💰 Калькулятор ЗП")

RATE = 10320
TAX = 0.05

user = st.radio("Кто считает?", ["Денис", "Анна"], horizontal=True)

day_type = st.selectbox("Тип дня", ["Будний день", "Выходной (Сб/Вс)"])
is_worked = st.checkbox("Отработал смену (8ч)", value=True) if day_type == "Будний день" else False
overtime = st.number_input("Часы чаноба (х1.5)", min_value=0.0, step=0.5, value=0.0)

if st.button(f"РАССЧИТАТЬ ДЛЯ {user.upper()}", use_container_width=True):
    if day_type == "Выходной (Сб/Вс)":
        total_before_tax = overtime * RATE * 1.5
    else:
        base = 8 * RATE if is_worked else 0
        total_before_tax = base + (overtime * RATE * 1.5)
    
    final_salary = total_before_tax * (1 - TAX)
    st.success(f"На руки: {final_salary:,.0f} вон")
