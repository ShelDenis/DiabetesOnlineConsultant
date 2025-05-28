import streamlit as st
import pickle
from sklearn.neighbors import KNeighborsClassifier

trans_dict = {
    'yn': {'Да': True, 'Нет': False},
    'sex': {'Женский': False, 'Мужской': True},
    'mark': {'Отлично': 1, 'Очень хорошо': 2, 'Хорошо': 3, 'Удовлетворительно': 4, 'Плохо': 5},
    'edu': {'Только дет. сад': 1, 'Младшая и средняя школа': 2,
            'Старшая школа': 3, 'Среднее профессиональное': 5, 'Высшее': 6},

}

def prediction_to_user():
    st.header("Проверка на наличие сахарного диабета")
    st.text("ИИ на основе введенных данных определит, подвержены ли вы "
            "заболеванию сахарным диабетом.")
    st.text("(ИИ не заменяет консультации со специалистом!)")
    st.image('data/neurodoc.jpg')

    up_bp = st.slider("Верхнее (систолическое) давление (мм.рт.ст):", 80, 160, 120)
    check_bounds(up_bp, 'Верхнее давление', 'мм.рт.ст', 80, 160)

    down_bp = st.slider("Нижнее (диастолическое) давление (мм.рт.ст):", 45, 95, 80)
    check_bounds(down_bp, 'Нижнее давление', 'мм.рт.ст', 45, 95)

    chol = st.slider("Уровень холестерина в крови (ммоль/л):", 1, 10, 5)
    check_bounds(chol, 'Уровень холестерина в крови', 'ммоль/л', 1, 10)

    check_chol = st.selectbox('Проверяли ли вы уровень холестерина в крови последние 5 лет? ', ['Да', 'Нет'])

    height = st.slider("Рост (см):", 130, 230,  175)
    check_bounds(height, 'Рост', 'см', 130, 230)

    weight = st.slider("Вес (кг):", 35, 250, 70)
    check_bounds(weight, 'Вес', 'кг', 35, 250)

    cigarettes = st.selectbox('Вы курите? ', ['Да', 'Нет'])

    stroke = st.selectbox('Был ли у Вас когда-нибудь инсульт?', ['Да', 'Нет'])

    heart_disease = st.selectbox('Была ли у Вас ишемическая болезнь сердца или инфаркт миокарда?', ['Да', 'Нет'])

    phys_activity = st.selectbox('Занимались ли Вы физической активностью за последние 30 дней?', ['Да', 'Нет'])

    fruits = st.selectbox('Употребляете ли Вы в пищу хотя бы один фрукт в день?', ['Да', 'Нет'])

    veggies = st.selectbox('Употребляете ли Вы в пищу хотя бы один овощ в день?', ['Да', 'Нет'])

    alcohol = st.selectbox('Вы считаете себя сильно пьющим человеком?', ['Да', 'Нет'])

    health_care = st.selectbox('У Вас есть медицинская страховка?', ['Да', 'Нет'])

    costly_doctor = st.selectbox('Вы часто не обращаетесь к докторам из-за дороговизны?', ['Да', 'Нет'])

    gen_health = st.selectbox('Оцените свой общий уровень здоровья:',
                              ['Отлично', 'Очень хорошо', 'Хорошо', 'Удовлетворительно', 'Плохо'])

    mental_days = st.slider("Сколько из последних 30 дней Вы чувствовали моральный стресс?", 0, 30, 0)
    check_bounds(mental_days, 'Дни морального стресса', 'дней', 0, 30)

    phys_days = st.slider("Сколько из последних 30 дней Вы чувстовали физическое недомогание?", 0, 30, 0)
    check_bounds(mental_days, 'Дни физического недомогания', 'дней', 0, 30)

    stairs = st.selectbox('Тяжело ли Вам подниматься по ступенькам?', ['Да', 'Нет'])

    sex = st.selectbox('Пол:', ['Женский', 'Мужской'])

    ages = []
    for i in range(18, 77, 4):
        ages.append(f'{i}-{i + 4}')
    ages.append('79 и более')
    age_dct = {}
    for i in range(1, len(ages) + 1):
        age_dct[ages[i - 1]] = i
    trans_dict['age'] = age_dct

    age = st.selectbox('Возраст:', ages)

    education = st.selectbox('Образование:', ['Только дет. сад', 'Младшая и средняя школа',
                                          'Старшая школа', 'Среднее профессиональное',
                                          'Высшее'])
    incomes = ['Менее 30 тыс. руб.']
    for i in range(30, 181, 30):
        incomes.append(f'{i}-{i + 30} тыс. руб.')
    incomes.append('Более 210 тыс. руб.')
    inc_dct = {}
    for i in range(1, len(incomes) + 1):
        inc_dct[incomes[i - 1]] = i
    trans_dict['inc'] = inc_dct
    income = st.selectbox('Ежемесячный доход:', incomes)

    if st.button('Узнать результат!'):
        if all([up_bp, down_bp, height, weight, chol]):
            bmi = float(weight) / ((float(height) / 100) ** 2)
            high_bp = False
            high_chol = False
            if float(up_bp) > 135 or float(down_bp) > 90:
                high_bp = True
            if float(chol) > 5.1:
                high_chol = True

            list_to_predict = [high_bp, high_chol, trv(check_chol, 'yn'),
                               bmi, trv(cigarettes, 'yn'), trv(stroke, 'yn'),
                               trv(heart_disease, 'yn'), trv(phys_activity, 'yn'),
                               trv(fruits, 'yn'), trv(veggies, 'yn'),
                               trv(alcohol, 'yn'), trv(health_care, 'yn'),
                               trv(costly_doctor, 'yn'), trv(gen_health, 'mark'),
                               int(mental_days), int(phys_days), trv(stairs, 'yn'),
                               trv(sex, 'sex'), trv(age, 'age'),
                               trv(education, 'edu'), trv(income, 'inc')]
            pred = None
            models_list = ['KNN', 'Boosting', 'Bagging', 'Stacking', 'Catboost', 'FCNN']
            for m in models_list:
                if m != 'Catboost':
                    ext = 'pkl'
                else:
                    ext = 'cbm'
                with open(f'models/{m.lower()}_model.{ext}', 'rb') as file:
                    model = pickle.load(file)
                    pred = model.predict([list_to_predict])

                if pred[0] == 0:
                    st.markdown(
                        f"""{m} считает, что 
                        <div style="background-color:green; padding:10px">
                            <h3>Вы здоровы!</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                elif pred[0] == 1:
                    st.markdown(
                        f"""{m} считает, что
                        <div style="background-color:yellow; padding:10px">
                            <h3>У вас есть небольшой риск заболеть сахарным диабетом. Будьте внимательны к своему здоровью!</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                elif pred[0] == 2:
                    st.markdown(
                        f"""{m} считает, что
                        <div style="background-color:red; padding:10px">
                            <h3>Есть вероятность того, что Вы больны сахарным диабетом. Рекомендуем обратиться к врачу.</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.error("Необходимо заполнить все поля!")


def check_bounds(var, name, measure, mn, mx):
    if var != "":
        try:
            val = float(var)

            if val > mx:
                st.error(f"{name} {val} {measure} превышает максимальное значение ({mx} {measure})")
            elif val < mn:
                st.error(f"{name} {val} {measure} ниже минимального значения ({mn} {measure})")
        except ValueError:
            st.warning("Ошибка! Необходимо ввести число.")


def trv(val, t):
    return trans_dict[t][val]




