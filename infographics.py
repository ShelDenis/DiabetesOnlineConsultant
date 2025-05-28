import streamlit as st
from load_data import load_data
import seaborn as sns
from matplotlib import pyplot as plt


def infographics():
    data = load_data()

    st.header("Инфографика")
    st.subheader("Факторы развития сахарного диабета")

    get_hist(data, 'Зависимость от потребления респондентом фруктов',
             '0 - не ест фрукты каждый день\n1 - ест фрукты каждый день', 'Fruits')

    get_hist(data, 'Зависимость от тяжести поднятия по ступенькам',
             '0 - легко подниматься по ступенькам\n1 - сложно', 'DiffWalk')

    get_hist(data, 'Зависимость от пола',
             '0 - ж\n1 - м', 'Sex')

    st.text("Распределение ИМТ")
    f_outlier = data[['BMI']]
    for column in f_outlier.columns:
        fig, ax = plt.subplots()
        f_outlier[column].hist(bins=20, log=True, ax=ax)
        st.pyplot(fig)

    income_counts = data['Income'].value_counts()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(income_counts, labels=income_counts.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Распределение значений поля Income')
    ax.axis('equal')

    st.pyplot(fig)

    incomes = ['1) Менее 30 тыс. руб.']
    for i in range(30, 181, 30):
        incomes.append(f'{int(i / 30) + 1}) {i}-{i + 30} тыс. руб.')
    incomes.append('8) Более 210 тыс. руб.')
    st.text('\n'.join(incomes))

    st.text("Тепловая карта порядковых признаков")
    int_data = data[['GenHlth', 'MentHlth', 'PhysHlth', 'Age', 'Education', 'Income']]
    fig, ax = plt.subplots(figsize=(16, 14))
    sns.heatmap(int_data.corr(numeric_only=True, method='spearman'), cmap="YlGnBu", annot=True)
    st.pyplot(fig)


def get_corr_graph(d, name, label):
    st.text(name)
    fig = sns.lmplot(x=label, y="Diabetes_012", data=d[:1000])
    st.pyplot(fig=fig.fig)


def get_boxplot(data, name, label):
    st.text(name)
    ax = data.boxplot(by=label, column=['Diabetes_012'], figsize=(7, 4), grid=True)
    fig = ax.get_figure()
    st.pyplot(fig)


def get_hist(data, name, desc, label):
    grouped = data.groupby(['Diabetes_012', label]).size().unstack(fill_value=0)

    fig, ax = plt.subplots()

    bar_width = 0.25

    index = range(len(grouped.index))

    colors = ['green', 'yellow', 'red']

    for i, column in enumerate(grouped.columns):
        ax.bar([i + bar_width * j for j in index], grouped[column], bar_width, color=[colors[j] for j in index],
               label=f'{label}={column}')

    ax.set_xlabel(label)
    ax.set_ylabel('Количество респондентов')
    ax.set_title('Гистограмма')
    ax.set_xticks([i + bar_width for i in index])
    ax.set_xticklabels(grouped.index)

    st.text(name)
    st.text(desc)
    st.text('Количество респондетнов:\n'
            'Зеленый - нет диабета\n'
            'Желтый - возможен диабет\n'
            'Красный - есть диабет')
    st.pyplot(fig)
