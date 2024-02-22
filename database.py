import certifi
import pandas as pd
import streamlit as st
from pymongo import MongoClient


st.title("Prueba de conexion mongo db")


def connection():
    return MongoClient("mongodb+srv://glider123ortega:cLXiTi6CgQZVJsa3@prediccion2024.kwtymza.mongodb.net/", tlsCAFile=certifi.where())

conexion = connection()

def getData():
    db = conexion.get_database("Prediccion")
    collections = db.get_collection("Ejempo1")
    items = collections.find()
    return list(items)

datos = getData()
st.subheader("DATOS")
st.dataframe(pd.DataFrame(datos))
