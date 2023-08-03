import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Dinner')
st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
st.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # Transforming data into normal form from JSON
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # Printing normalized data into table format
    return fruityvice_normalized
  
st.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
    if not fruit_choice:
        st.error("Please select a fruit to get information")
    else:
        st.write('The user entered ', fruit_choice)
        back_from_function = get_fruityvice_data(fruit_choice)
        st.dataframe(back_from_function)
except URLError as e:
    st.error()


# snowflake.connector needs to be fixed since the code was previously incorrect
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
st.header("The fruit load list contains:")
#Snowflake-related functions
def get_fruit_load_list():
        with my_cnx.cursor() as my_cur
              my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
             return my_cur.fetchall()
#Add a button to load gthe fruit
if st.button('Get Fruit Load List'):
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        my_data_rows = get_fruit_load_list()
        st.dataframe(my_data_rows)

st.stop();
add_my_fruit = st.text_input('What fruit would you like to add?', 'jackfruit')
my_cur.execute("insert into fruit_load_list values ('" + add_my_fruit + "')")
st.write('Thanks for adding', add_my_fruit)
st.stop()
