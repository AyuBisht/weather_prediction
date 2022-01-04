import pytz
import streamlit as st
import pyowm
import time
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt

degree_sign= u'\N{DEGREE SIGN}'

#____________________________________________________________________________________________________________________________________________________________
##     FRONT END

#title and placeholer text using streamlit
st.title("5 Day Weather Forecast")
st.write("### Write the name of a City (India) and select the Temperature Unit and Graph Type from the sidebar")

#input city name using single line text widget and storing it in a var
place = st.text_input("Name of the City:") #arguements as label and value when text widget is first rendered

if place==None:
    st.write("Input a CITY!")

#input temperature unit and graph type using select widget and storing it in a var
Unit = st.selectbox("Select temperature unit", ("celsius", "fahrenheit"))
Graph_type = st.selectbox("Select graph type", ("Line Graph","Bar Graph"))

#creating the submit button
Submit = st.button("Submit")

#____________________________________________________________________________________________________________________________________________________________    
##     GET DATA FROM API AND ORGANIZE IT

#API key from OpenWeatherMap website
#owm is an OWM object
#fetching the data from pyowm
owm = pyowm.OWM('1f84abe6981c2014ea9e1f94e2b8459a')
mgr = owm.weather_manager()
    
Days = []
Min_temperature = []   
Max_temperature = []

def gmt_to_ist(unix_gmt):
    ist = pytz.timezone('Asia/Kolkata')
    gmt = pytz.timezone('GMT')
    date = datetime.utcfromtimestamp(unix_gmt)
    date = gmt.localize(date)
    indian_time = date.astimezone(ist)

    return indian_time


def get_data():
    forecast = mgr.forecast_at_place(place, '3h').forecast
    for weather in forecast:
        day = gmt_to_ist(weather.reference_time())
        date = day.date()
        if (date == gmt_to_ist(time.time()).date()):
            continue
        if date not in Days:
            Days.append(date)
            Min_temperature.append(None)
            Max_temperature.append(None)
            
        temperature = weather.temperature(Unit)['temp']
        if not Min_temperature[-1] or temperature < Min_temperature[-1]:
            Min_temperature[-1] = temperature
        if not Max_temperature[-1] or temperature > Max_temperature[-1]:
            Max_temperature[-1] = temperature

    

#_________________________________________________________________________________________________________________________________________________________________
###       PLOT THE GRAPH
 
def init_plot():
    fig = plt.figure('PyOWM Weather', figsize=(5,4))  
    plt.xlabel('Day')
    plt.ylabel(f'Temperature ({degree_sign}{Unit})' )
    plt.title('Weekly Forecast') 
    return fig

def label_xaxis(days):
    plt.xticks(days) #This takes the list of datetime objects that were passed in as a parameter and uses them for the x-axis labels
    axes = plt.gca() # calling the gca() method to get the axes of the plot
    xaxis_format = dates.DateFormatter('%m/%d') #the DateFormatter() method from Matplotlib is used to specify a format of the month and day separated by a slash.
    axes.xaxis.set_major_formatter(xaxis_format)

def plot_BarGraph(days, temp_min, temp_max):
    days = dates.date2num(days)    
    plt.bar(days-.25, temp_min, width=0.5, color='blue')
    plt.bar(days+.25, temp_max, width=0.5, color='orange')

def plot_LineGraph(days, temp_min, temp_max):
    days = dates.date2num(days)
    plt.plot(days, temp_min, color='blue')
    plt.plot(days, temp_max, color='orange')

##___________________________________________________________________________________________________________________________________________________________________
#             MAIN FUNCTION 


if __name__ == '__main__':
    if Submit:        
        get_data()
        if Graph_type=="Bar Graph":
            fig = init_plot()
            plot_BarGraph(Days, Min_temperature, Max_temperature)            
            label_xaxis(Days)
            st.pyplot(fig)        
        else:
            fig = init_plot()
            plot_LineGraph(Days, Min_temperature, Max_temperature)            
            label_xaxis(Days)
            st.pyplot(fig)
               
        st.write("### Maximum And Minimum Temperature\n")
        for (day, min, max) in zip(Days, Min_temperature, Max_temperature):
            st.write(f"{day} : {min}{degree_sign} -- {max}{degree_sign}")
            
            






