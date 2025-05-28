import streamlit as st
from developer import developer
from dataset_description import dataset_description
from infographics import infographics
from prediction_to_user import prediction_to_user


def select_page():
    page = st.sidebar.selectbox("Выбрать страницу",
                                ["Информация о разработчике",
                                 "Описание датасета",
                                 "Визуализация зависимостей",
                                 "Предсказание модели ML"
                                 ])

    if page == "Информация о разработчике":
        developer()
    elif page == "Описание датасета":
        dataset_description()
    elif page == 'Визуализация зависимостей':
        infographics()
    elif page == 'Предсказание модели ML':
        prediction_to_user()