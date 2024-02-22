import certifi
import pandas as pd
import streamlit as st
from pymongo import MongoClient

st.title("Prueba de conexión a MongoDB")

@st.cache_resource()
def connection():
    return MongoClient("mongodb+srv://"+st.secrets["DB_USERNAME"]+":"+st.secrets["DB_PASSWORD"]+"@prediccion2024.kwtymza.mongodb.net/", tlsCAFile=certifi.where())

conexion = connection()

@st.cache_data(ttl=60)
def getData():
    db = conexion.get_database("sample_restaurants")
    collections = db.get_collection("restaurants")
    items = collections.find()
    return list(items)

#Insertar una base de datos paso 1/2
#def insertData(newData):
    #db = conexion.get_database("sample_restaurants")
   # nuevaCollection = (db.create_collection("inventario3"))
    # nuevaCollection.insert_many(newData)

def insertNewData(newData):
    db = conexion.get_database("sample_restaurants")
    nuevaCollection = db.get_collection("sample_restaurants")
    nuevaCollection.insert_many(newData)


datos = getData()

# DataFrame original eliminando filas con valores nulos
df_original = pd.DataFrame(datos).dropna()

# DataFrame sin la columna address
df_sin_address = df_original.drop(columns=['address'])

# Solo las columnas cuisine y name
df_cuisine_name = df_original[['cuisine', 'name']]

st.subheader("TABLA ORIGINAL")
st.dataframe(df_original)

st.subheader("TABLA CON ADDRESS ELIMINADO")
st.dataframe(df_sin_address)

st.subheader("TABLA SOLO CON COLUMNAS 'cuisine' Y 'name'")
st.dataframe(df_cuisine_name)


#Insertar una base de datos paso 2/2
#dfWalmart = pd.read_csv("datos/Walmart.csv")
#st.dataframe(dfWalmart.head())

#Walmart2Collection = dfWalmart.to_dict(orient="records")
#st.write(Walmart2Collection[0:3])
#insertData(Walmart2Collection)


#Crear formulario para actualizar la bd
st.title("Ingresar nuevos datos")

with st.form("my form"):
    nombreProducto = st.text_input("Nombre del producto")
    nombreLocacion = st.text_input("Locacion")
    fecha = st.date_input("Fecha de registro")
    calificacion = st.number_input("Elije una calificación:",0,10)
    enviado = st.form_submit_button("Enviar Datos")

    if enviado:
        datoNuevo = {}
        datoNuevo["id"] = 100
        datoNuevo["name"] =nombreProducto
        datoNuevo["location"] = nombreLocacion
        datoNuevo["Date"] = fecha
        datoNuevo["Rating"] = calificacion
        insertNewData(datoNuevo)