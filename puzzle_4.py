import time
import json
import os
from pathlib import Path
import streamlit as st
import random

st.title("Kitchen Orientation")

list_of_word_pairs = ["Gas", "Water Pipe", "Fridge", "Power Outlet", "Sink", "Stove" ,"Fire extinguisher", "Wall Mount"]

ans1 = st.multiselect("Place the correct Layout of the Kitchen", options = list_of_word_pairs, max_selections = 2,key = 1)
ans2 = st.multiselect("Place the correct Layout of the Kitchen", options = list_of_word_pairs, max_selections = 2,key = 2 )
ans3 = st.multiselect("Place the correct Layout of the Kitchen", options = list_of_word_pairs, max_selections = 2,key = 3)
ans4 = st.multiselect("Place the correct Layout of the Kitchen", options = list_of_word_pairs, max_selections = 2, key = 4)

answers = [ans1, ans2, ans3, ans4]

counter = 0
for answer in answers:
    if answer in [["Gas", "Stove"],["Stove", "Gas"]]:
        st.toast("Installed a stove")
        counter += 1
    elif answer in [["Water Pipe", "Sink"],["Sink", "Water Pipe"]]:
        st.toast("Installed a sink")
        counter += 2
    elif answer in [["Fire extinguisher", "Wall Mount"],["Wall Mount", "Fire extinguisher"]]:
        st.toast("Installed a fire extinguisher")
        counter += 3
    elif answer in [["Power Outlet", "Fridge"],["Fridge", "Power Outlet"]]:
        st.toast("Installed a fridge")
        counter += 4
    else:
        counter = 0
if counter == 10:
    st.ballons()
    st.success("You now have kitchen!!")