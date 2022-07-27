import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


streamlit.title('My Parents New Healthy Dinner')
   
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# here there was Panda import

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

#here there was import request
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

def get_fruityvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized
   

#new section to display Fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?','')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:
      #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      back_from_function=get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
except URLError as e:
   streamlit.error()
      
      
# streamlit.text(fruityvice_response.json())

# normalising json verion 
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# wscreen output
#streamlit.dataframe(fruityvice_normalized)



#here there was import snowflake connector
streamlit.header("View our fruit list - Add Your Favorites!")
#snowflake-related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * from fruit_load_list")
      return my_cur.fetchall()
# add a button to load the fruit
if streamlit.button('Get Fruit list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows=get_fruit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)
      
# allow the end user to enter another fruit to the list
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
      return "Thanks for adding " + new_fruit
   
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function=insert_row_snowflake(add_my_fruit)
   my_cnx.close()
   streamlit.text(back_from_function)

      
      
#my_cur = my_cnx.cursor()

#my_data_rows = my_cur.fetchall()
#don't run anything past here while we troubleshoot
#streamlit.stop()






#this not works for now but it will soon


