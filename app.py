import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

st.title('Анализ зарплат в России за 2000-2023 годы')
image = Image.open('img.jpg')
st.image(image)

zp = pd.read_csv('zarplata.csv', index_col=0)
inflat = pd.read_csv("inflation.csv",index_col=0)

years = np.arange(2000, 2024)
zp.columns = years

show_zp = st.sidebar.checkbox('Показать данные по зарплатам')
if show_zp == True:
    st.dataframe(zp)
    for i in range(3):
        fig = plt.figure(figsize=(7, 4))
        sns.lineplot(x = zp.columns, y = zp.iloc[i])
        plt.title(zp.index[i])
        plt.xlabel('Год')
        plt.ylabel('Зарплата, руб')
        st.pyplot(fig)

infl = inflat.iloc[-24:][['Год','Всего']].reset_index(drop = True)
infl['Всего'] = infl['Всего'].str.replace(',', '.').astype('float')

inf = infl['Всего'].values
inf_total = [inf[0]]
for i in range(1, len(inf)):
    new_inf = inf_total[-1] + inf[i] + (inf_total[-1] * inf[i] / 100)
    inf_total.append(new_inf)

show_infl = st.sidebar.checkbox('Показать данные по инфляции')
if show_infl == True:
    st.dataframe(inflat)
    fig2 = plt.figure(figsize=(7, 4))
    sns.lineplot(x = years, y = inf_total)
    plt.xlabel('Год')
    plt.ylabel('Инфляция, %')
    plt.title('Накопленная инфляция')
    st.pyplot(fig2)

show_zp_infl = st.sidebar.checkbox('Показать реальную зарплату с учетом инфляции')
if show_zp_infl == True:
    inf = infl['Всего'].values
    for i in range(3):

        zpl = zp.iloc[i, 0]
        zp_inf = [zpl]
        for j in range(1, len(inf)):
            zpl = zpl * (1 + inf[j] / 100)
            zp_inf.append(zpl)
        zp_final = [zp.iloc[i, x] - zp_inf[x] + zp.iloc[i, 0] for x in range(len(inf))]

        fig3 = plt.figure(figsize=(7, 4))
        sns.lineplot(x=zp.columns, y=zp.iloc[i], label='Текущая зарплата')
        sns.lineplot(x=zp.columns, y=zp_inf, label='Инфляция зарплаты')
        sns.lineplot(x=zp.columns, y=zp_final, label='Реальная зарплата с учетом инфляции')
        plt.xlabel('Год')
        plt.ylabel('Зарплата, руб')
        plt.title(zp.index[i])
        plt.legend()
        st.pyplot(fig3)

show_dinamika = st.sidebar.checkbox('Показать динамику изменения реальной зарплаты')
if show_dinamika == True:
    for j in range(3):

        dif_inf = []
        for i in range(len(inf) - 1):
            zpl = zp.iloc[j, i + 1]
            zp_inf = zp.iloc[j, i] * (1 + inf[i] / 100)
            res = zpl - zp_inf
            dif_inf.append(res)

        fig4 = plt.figure(figsize=(12, 4))
        sns.barplot(x=years[1:], y=dif_inf, label='Изменение зарплат с учетом инфляции')
        plt.xlabel('Год')
        plt.ylabel('Зарплата')
        plt.title(zp.index[j])
        plt.legend()
        st.pyplot(fig4)