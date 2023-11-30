# Native libraries
import os
import math
# Essential Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
# Dalam membuat proyek ini, saya menggunakan google drive untuk menyimpan data set saya

import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


raw_data = pd.read_csv('dashboard/main_data.csv')

data1 = raw_data.copy()

indeks_musim=['Spring', 'Summer', 'Fall', 'Winter']
indeks_libur=['Not Holiday', 'Holiday']
indeks_cuaca=['Clears', 'Mist or Cloudy', 'Light Rain or Light Snow', 'Heavy Rain or Heavy Snow']
indeks_hari=['Sunday', 'Monday', 'Tuesday', 'Wednesday', "Thursday", "Friday", "Saturday"]
indeks_tahun=['2011', '2012']
indeks_bulan=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
indeks_harikerja=['Not Working Day', 'Working Day']

data1['season'] = data1['season'].replace([1,2,3,4], indeks_musim)
data1['holiday'] = data1['holiday'].replace([0,1], indeks_libur)
data1['weathersit'] = data1['weathersit'].replace([1,2,3,4], indeks_cuaca)
data1['weekday'] = data1['weekday'].replace([0,1,2,3,4,5,6], indeks_hari)
data1['mnth'] = data1['mnth'].replace([1,2,3,4,5,6,7,8,9,10,11,12], indeks_bulan)
data1['yr'] = data1['yr'].replace([0,1], indeks_tahun)
data1['workingday'] = data1['workingday'].replace([0,1], indeks_harikerja)
data1["dteday"] = pd.to_datetime(data1["dteday"])
min_date = data1["dteday"].min()
max_date = data1["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://idcamp.ioh.co.id/images/indosat-x-idcamp-logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Range',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
data = data1[(data1["dteday"] >= str(start_date)) & 
                (data1["dteday"] <= str(end_date))]

st.header('Bike Sharing Analysis')
tab1, tab2, tab3 = st.tabs(["About Bike Sharing", "Bike Sharing Data in Nutshell", "More About This Bike Sharing Data"])
with tab1:
    st.image("https://www.infobdg.com/v2/wp-content/uploads/2017/07/IMG_9904-696x464.jpg")
    st.write("""A bicycle-sharing system, bike share program, public bicycle scheme, or public bike share (PBS) scheme, is a shared transport service where bicycles are available for shared use by individuals at low cost.

The programmes themselves include both docking and dockless systems, where docking systems allow users to rent a bike from a dock, i.e., a technology-enabled bicycle rack and return at another node or dock within the system – and dockless systems, which offer a node-free system relying on smart technology. In either format, systems may incorporate smartphone web mapping to locate available bikes and docks. In July 2020, Google Maps began including bike share systems in its route recommendations.

With its antecedents in grassroots mid-1960s efforts; by 2022, approximately 3,000 cities worldwide offer bike-sharing systems, e.g., Dubai, New York, Paris, Montreal and Barcelona.""")
    st.write("Source [link](https://en.wikipedia.org/wiki/Bicycle-sharing_system)")

with tab2:
    st.header("Bike Sharing Data in Nutshell")
    st.write("You can use time range in the sidebar :sparkles:")

    ##Lineplot 

    st.subheader('Daily Bike Rented')

    col1, col2 = st.columns(2)
    
    with col1:
        total_rental = data['cnt'].sum()
        st.metric("Total Rented Bikes", value=total_rental)
    
    with col2:
        average = data['cnt'].mean()
        st.metric("Average Daily Rented bikes", value=average)
    
    fig, ax = plt.subplots(figsize=(17, 8))
    ax.plot(
        data["dteday"],
        data["cnt"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    
    st.pyplot(fig)


    ##Pie Chart
    st.subheader("Our Costumer")
    col1, col2 = st.columns(2)
    with col1:
        total_member = data['registered'].sum()
        st.metric("The total number of bicycles rented using a membership.", value=total_member)

    with col2:
        total_casual = data['casual'].sum()
        st.metric("The total number of bicycles rented using a non-membership.", value=total_casual)
   
    fig, ax = plt.subplots()
    ax.pie([data["casual"].sum(),data["registered"].sum()], labels = ["Non-Member","Member"], explode=[0,0.2], colors = ["#D3D3D3","#72BCD4"]) 
    st.pyplot(fig)


    ##Plot terakhir
    st.subheader("Customer Behaviour")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(20, 10))
        seasons=data.groupby(by="season").agg({"cnt": "sum"}).reset_index()
        colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        sns.barplot(
        y="cnt", 
        x="season",
        data=seasons.sort_values(by="cnt", ascending=False),
        palette=colors_)
        ax.set_title("Best Season to Cycling", loc="center", fontsize=50)
        ax.set_ylabel("Total Rental Bikes in million", fontsize=20)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=35)
        ax.tick_params(axis='y', labelsize=30)
        st.pyplot(fig)
        
    
    with col2:
        fig, ax = plt.subplots(figsize=(20, 10))
        
        colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
        wea=data.groupby(by="weathersit").agg({"cnt": "sum"}).reset_index()

        colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3"]
        sns.barplot(
        y="cnt",
        x="weathersit",
        data=wea.sort_values(by="cnt", ascending=False),
        palette=colors_)
        ax.set_title("Best Weather to Cycling", loc="center", fontsize=50)
        ax.set_ylabel("Total Rental Bikes in million", fontsize=20)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=35)
        ax.tick_params(axis='y', labelsize=30)
        st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(20, 10))
    weekday=data.groupby(by="weekday").agg({"cnt": "sum"}).reset_index()

    colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3" , "#D3D3D3"]
    sns.barplot(
        x="cnt",
        y="weekday",
        data=weekday.sort_values(by="cnt", ascending=False),
        palette=colors_)
    ax.set_title("Best Day to Cycling", loc="center", fontsize=30)
    ax.set_ylabel(None)
    ax.set_xlabel("Total Rental Bikes", fontsize=20)
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)

with tab3:
    data2=data1.copy()
    st.header("More About This Bike Sharing Data")
    tab3a, tab3b, tab3c = st.tabs(["Season Effects", "Weather Effects", "Day Effect"])
    with tab3a:    
        st.subheader('Influence of Season on Rental Bikes')
        colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        
        seasons1=data2.groupby(by="season").agg({"cnt": "sum"}).reset_index()
        fig, ax = plt.subplots(figsize=(20, 10))
        sns.barplot(
        y="cnt", 
        x="season",
        data=seasons1.sort_values(by="cnt", ascending=False),
        palette=colors_)
        ax.set_title("Best Season to Cycling", loc="center", fontsize=35)
        ax.set_ylabel("Total Rental Bikes in million", fontsize=25)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=25)
        ax.tick_params(axis='y', labelsize=25)
        st.pyplot(fig)
        with st.expander("Does the season affect Rental Bikes?"):
            st.write("From the plot above, bicycles are most frequently rented in the fall, and the least rented in the spring.")

            fall=data2.loc[data2['season'] == 'Fall', ['cnt']]
            fall=fall['cnt'].to_numpy()
            fall=fall.transpose()

            winter=data2.loc[data2['season'] == 'Winter', ['cnt']]
            winter=winter['cnt'].to_numpy()
            winter=winter.transpose()

            summer=data2.loc[data2['season'] == 'Summer', ['cnt']]
            summer=summer['cnt'].to_numpy()
            summer=summer.transpose()

            spring=data2.loc[data2['season'] == 'Spring', ['cnt']]
            spring=spring['cnt'].to_numpy()
            spring=spring.transpose()

            fig = plt.figure(figsize =(10, 7))
            
            # Creating axes instance
            ax = fig.add_axes([0, 0, 1, 1])
            
            # Creating plot
            bp = ax.boxplot([fall, winter, summer, spring])
            plt.xticks([1,2,3,4],["fall", "winter", "summer", "spring"])
            ax.set_title("Box Plot for Each Season", loc="center", fontsize=30)
            ax.set_ylabel("Daily Total Rental Bikes", fontsize=20)
            ax.set_xlabel(None)
            ax.tick_params(axis='x', labelsize=25)
            ax.tick_params(axis='y', labelsize=20)
            # show plot
            st.pyplot(fig)
            st.write("From this Boxplot, the data distribution during the fall, winter, and summer seasons appears similar. To test this similarity, ANOVA (to test mean equality) or Kruskall-Wallis (to test median equality) will be used. Before proceeding to these tests, the data will first be tested for normality, with the null hypothesis being that the data is normally distributed.")
            musim=[fall,winter,summer,spring]
            musim_string=["fall","winter",'summer','spring']
            st.write("Saphiro Wilk Normality Test:")
            for i in range(len(musim)):
                st.write("for", musim_string[i], ":" , stats.shapiro(musim[i]))
            st.write("Reject the null hypothesis when α > p-value, which means the data is not normally distributed. It is found that for significance levels (α) ranging from 1% to 10%, only the winter data is normally distributed. Therefore, ANOVA cannot be performed. Consequently, a Kruskall-Wallis test will be conducted with the null hypothesis that the median of all data is the same.")
            st.write("Kruskal Wallis:")
            st.write(stats.kruskal(fall,winter,summer,spring))
            st.write('For significance levels (α) ranging from 1% to 10%, the null hypothesis is rejected, indicating a difference in the median of the four seasons. In other words, the seasons influence the number of bicycles rented, contradicting the assumption I made when observing the visualization.')

    with tab3b:
        st.subheader('Influence of Weather on Rental Bikes')
        fig, ax = plt.subplots(figsize=(20, 10))
            
        colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"]
    
        wea=data2.groupby(by="weathersit").agg({"cnt": "sum"}).reset_index()

        colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3"]
        sns.barplot(
        y="cnt",
        x="weathersit",
        data=wea.sort_values(by="cnt", ascending=False),
        palette=colors_)
        ax.set_title("Best Weather to Cycling", loc="center", fontsize=35)
        ax.set_ylabel("Total Rental Bikes in million", fontsize=25)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=25)
        ax.tick_params(axis='y', labelsize=25)
        st.pyplot(fig)
        with st.expander("Does the weather affect Rental Bikes?"):
            st.write("From the above plot, bicycles are most frequently rented during clear weather, and the least rented during light rain/snow.")
            cerah=data2.loc[data2['weathersit'] == 'Clears', ['cnt']]
            cerah=cerah['cnt'].to_numpy()
            cerah=cerah.transpose()

            berawan=data2.loc[data2['weathersit'] == 'Mist or Cloudy', ['cnt']]
            berawan=berawan['cnt'].to_numpy()
            berawan=berawan.transpose()

            hujan=data2.loc[data2['weathersit'] == 'Light Rain or Light Snow', ['cnt']]
            hujan=hujan['cnt'].to_numpy()
            hujan=hujan.transpose()



            fig = plt.figure(figsize =(10, 7))

            # Creating axes instance
            ax = fig.add_axes([0, 0, 1, 1])

            # Creating plot
            bp = ax.boxplot([cerah, berawan, hujan])
            plt.xticks([1,2,3],[ 'Clears', 'Mist or Cloudy', 'Light Rain or Light Snow'])
            ax.set_title("Box Plot for Each Weather", loc="center", fontsize=30)
            ax.set_ylabel("Daily Total Rental Bikes", fontsize=20)
            ax.set_xlabel(None)
            ax.tick_params(axis='x', labelsize=25)
            ax.tick_params(axis='y', labelsize=20)
            # show plot
            st.pyplot(fig)
            st.write('From this Boxplot, the data distribution during clear and cloudy skies appears similar. To test this similarity, ANOVA (to test mean equality) or Kruskall-Wallis (to test median equality) will be used. Before proceeding to these tests, the data will first be tested for normality, with the null hypothesis being that the data is normally distributed.')
            cuaca=[cerah, berawan, hujan]
            cuaca_string=['Clears', 'Mist or Cloudy', 'Light Rain or Light Snow']
            st.write("Saphiro Wilk Normality Test:")
            for i in range(len(cuaca)):
                st.write("For", cuaca_string[i], ":" , stats.shapiro(cuaca[i]))
            st.write('Reject the null hypothesis when α > p-value, indicating that the data is not normally distributed. It is found that for significance levels (α) ranging from 1% to 9%, only light rain is normally distributed. Therefore, ANOVA cannot be performed. Consequently, a Kruskall-Wallis test will be conducted with the null hypothesis that the median of all data is the same.')
            st.write("Kruskal Wallis:")
            st.write(stats.kruskal(cerah, berawan, hujan))
            st.write('For significance levels (α) ranging from 1% to 10%, the null hypothesis is rejected, indicating a difference in the median of the three weather conditions. In other words, weather conditions influence the number of bicycles rented, contradicting the assumption I made when observing the visualization.')

    with tab3c:
        st.subheader('Influence of Day on Rental Bikes')
        fig, ax = plt.subplots(figsize=(20, 10))
        weekday=data2.groupby(by="weekday").agg({"cnt": "sum"}).reset_index()

        colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3" , "#D3D3D3"]
        sns.barplot(
            x="cnt",
            y="weekday",
            data=weekday.sort_values(by="cnt", ascending=False),
            palette=colors_)
        ax.set_title("Best Day to Cycling", loc="center", fontsize=30)
        ax.set_ylabel(None)
        ax.set_xlabel("Total Rental Bikes", fontsize=20)
        ax.tick_params(axis='y', labelsize=20)
        ax.tick_params(axis='x', labelsize=15)
        st.pyplot(fig)
        with st.expander("Does the day affect Rental Bikes?"):
            monday=data2.loc[data2['weekday'] == 'Monday', ['cnt']]
            monday=monday['cnt'].to_numpy()
            monday=monday.transpose()

            tuesday=data2.loc[data2['weekday'] == 'Tuesday', ['cnt']]
            tuesday=tuesday['cnt'].to_numpy()
            tuesday=tuesday.transpose()



            wednesday=data2.loc[data2['weekday'] == 'Wednesday', ['cnt']]
            wednesday=wednesday['cnt'].to_numpy()
            wednesday=wednesday.transpose()

            thursday=data2.loc[data2['weekday'] == 'Thursday', ['cnt']]
            thursday=thursday['cnt'].to_numpy()
            thursday=thursday.transpose()

            friday=data2.loc[data2['weekday'] == 'Friday', ['cnt']]
            friday=friday['cnt'].to_numpy()
            friday=friday.transpose()

            saturday=data2.loc[data2['weekday'] == 'Saturday', ['cnt']]
            saturday=saturday['cnt'].to_numpy()
            saturday=saturday.transpose()

            sunday=data2.loc[data2['weekday'] == 'Sunday', ['cnt']]
            sunday=sunday['cnt'].to_numpy()
            sunday=sunday.transpose()

            fig = plt.figure(figsize =(10, 7))

            # Creating axes instance
            ax = fig.add_axes([0, 0, 1, 1])

            # Creating plot
            bp = ax.boxplot([monday, tuesday, wednesday, thursday, friday, saturday, sunday])
            plt.xticks([1,2,3,4,5,6,7],['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
            # show plot
            ax.set_title("Box Plot for Each Day", loc="center", fontsize=30)
            ax.set_ylabel("Daily Total Rental Bikes", fontsize=20)
            ax.set_xlabel(None)
            ax.tick_params(axis='x', labelsize=20)
            ax.tick_params(axis='y', labelsize=20)
            # show plot
            st.pyplot(fig)

            st.write('From this Boxplot, the data distribution across all days appears similar. to test this similarity, ANOVA (to test mean equality) or Kruskall-Wallis (to test median equality) will be used. Before proceeding to these tests, the data will first be tested for normality, with the null hypothesis being that the data is normally distributed.')
            hari=[monday, tuesday, wednesday, thursday, friday, saturday, sunday]
            hari_string=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            st.write("Saphiro Wilk Normality Test:")
            for i in range(len(hari)):
                st.write("For", hari_string[i], ":" , stats.shapiro(hari[i]))
            st.write('Reject the null hypothesis when α > p-value, indicating that the data is not normally distributed. For significance levels (α) ranging from 1% to 10%, it is found that Tuesday and Thursday have very small values (< 0.01), meaning Tuesday and Thursday come from non-normally distributed data. Therefore, ANOVA cannot be conducted. Consequently, a Kruskall-Wallis test will be performed with the null hypothesis that the median of all data is the same.')
            st.write("Kruskal Wallis:")
            st.write(stats.kruskal(monday, tuesday, wednesday, thursday, friday, saturday, sunday))
            st.write('For significance levels (α) ranging from 1% to 10%, the null hypothesis is not rejected, indicating NO difference in the median of the seven days. In other words, the average number of bicycles rented can be considered similar every day, aligning with the assumption I made when observing the visualization.')
            
            
