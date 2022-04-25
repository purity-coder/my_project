#Import the necessary libraries
#pip install "scikit-learn==0.19.0"
import streamlit as st
import pickle
import pandas as pd
from PIL import Image
import time
from sklearn import *

#Load the model
def load_model():
    with open('chosen_model.pkl','rb') as file:
        load_data=pickle.load(file)
    return load_data

load_data = load_model()
model = load_data["model"]
mon_encoder = load_data["le_mon"]
ty_encoder = load_data["le_ty"]
polynom = load_data["poly"]

#This is for the title
st.title('IN-HOUSE SMART DUSTBIN CLIENT APP')


#Welcoming the user and telling them how the system works
"""Welcome and feel free to use this smart dustbin app that will check the level of waste in the dustbin and automatically empty this waste when necessary """



#Here am going to attach a photo

#User data
st.header('Enter the date(day,month) and the bin you want to detect the waste level ')

#Note


#Store the input 'MONTH' selected by the user and tell them what they have choosen
month=('May','December', 'March','October', 'June', 'January',
        'November', 'February', 'July', 'April', 'September', 'August')

chosen_month=st.selectbox('Select the month of the year',month)

#Store the input 'DAY' entered by the user and tell them what they have choosen
day = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)

chosen_day = st.selectbox('Select the day',day)

#Store the input 'WASTE' that is contained in the bin
waste= {"My Bin" : 'Yard Waste'}


chosen_type=st.selectbox('Select the bin you want to monitor',waste)
st.write('You currently have just one bin:',chosen_type)
st.write('NB: We can keep track of more than one bins,you can always add more bins to this system')

#What is contained in the bin
for chosen_type,value in waste.items():
    answer = value

 #Make a dataframe using the user input data
input_data = {'MONTH':chosen_month,'DAY':chosen_day,'BIN':answer}
input_df = pd.DataFrame(input_data,index=[0])

#Show the user what they have entered
st.header('You chose')
st.table(input_df)

#Output
ok = st.button("MONITOR")
if ok:
#CLEANING USER INPUT DATA
    Z = input_df[['DAY','MONTH','BIN']]
    Z['MONTH'] = mon_encoder.transform(Z['MONTH'])
    Z['BIN'] = ty_encoder.transform(Z['BIN'])
    Z[['DAY']] = preprocessing.normalize(Z[['DAY']])
    Z = polynom.fit_transform(Z)

#Contacting the cloud 
    waste_total = model.predict(Z)

#This if statement is to inform the managing personnel more about the level of waste

    if(waste_total[0]<=100):
          st.markdown(f"The garbage level is at [**{waste_total[0]:.2f} TONS**] mark.It is still a quarter full")
    elif(waste_total[0]>100 and waste_total[0]<=400):
          st.markdown(f"The garbage level is at [**{waste_total[0]:.2f} TONS**] mark.It is halfway full ")
    else:
        st.markdown(f"The garbage level is at [**{waste_total[0]:.2f} TONS**] mark.The garbage is full!.No need to worry I am taking care of this in a moment")
        st.write("""*Contacting the server motor to empty the bin......*""")
        time.sleep(20)
        empty = waste_total[0]-waste_total[0]
        st.subheader(f"The bin was successfully emptied, the garbage level is now at [*{empty}*] TONS")