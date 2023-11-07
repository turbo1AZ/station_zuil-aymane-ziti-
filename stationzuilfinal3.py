#import de benodigde modules
import tkinter as tk
import psycopg2
from tkinter import *
import requests

#maakt een tkinter venster
root = Tk()
root.title("Zuil_Aymane")
root.resizable(width=False, height=False)
canvas = Canvas(root, width=1400, height=900, bg="#FFC917")

#maakt een funcite om weer berichten op te halen
def weer(city_name, api_key):
    #krijgt hier toagang op door de api key
    base_url =f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={api_key}&units=metric"
    try:
        #vraagt het op
        response = requests.get(base_url)

        if response.status_code == 200:
            data = response.json()
            #bij een succses volle aanvraag kopelt hij dit aan een label
            label.config(text=f"het weer in \n {city_name} \n is {data['main']['temp']}ºC. \n Feels like {data['main']['feels_like']}°C. \n {data['weather'][0]['description']}. Wind speed: {data['wind']['speed']} m/s.)")
        else:
            print("Failed to retrieve weather data. Status code:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("An error occurred during the request:", e)
        return None

canvas.pack_forget()
key = "129d91e31beba5e08c872efad56b2eab"

#,maakt knoppen dat als ze worden gedrukt ze de weer functie terug geven
def knopDenBosch_click():
    weer("Den Bosch,NL", key)
    canvas.pack()

def knopUtrecht_click():
    weer("Utrecht,NL", key)
    canvas.pack()

def knopOss_click():
    weer("Oss,NL", key)
    canvas.pack()
#maakt knoppen voor de verschilende steden  met  tekstlabels en koppelt ze aan de functies
knopDenBosch = tk.Button(root, text="Den Bosch", command=knopDenBosch_click, width=100, height=2)
knopUtrecht = tk.Button(root, text="Utrecht", command=knopUtrecht_click, width=100, height=2)
knopOss = tk.Button(root, text="Oss", command=knopOss_click, width=100, height=2)

#laad abeeldingen voor de instalaties functie die worden getoond bij corect gerbuik.
image_pr = tk.PhotoImage(file="img_pr.png")
image_lift = tk.PhotoImage(file="img_lift.png")
image_ovfiets = tk.PhotoImage(file="img_ovfiets.png")
image_toilet = tk.PhotoImage(file="img_toilet.png")

#maakt een label voor het tonen van informatie
label = tk.Label(root, text="", font=("Calibri", 10, "bold"), bg="#FFC917")
#plaatst de knoppen en de label op de spcifieke plekken.
knopDenBosch.pack()
knopUtrecht.pack()
knopOss.pack()
label.place(x=1150, y=15)

#maakt een conectie met de server.
conn = psycopg2.connect(
    host='172.166.133.82',
    database='station_zuil',
    user='postgres',
    password='aymane21',
    port='5432')




def instalaties (stad, foto_y_coordinaten):
    cursor = conn.cursor()
    #stelt de query weer op
    query = "SELECT * FROM station_service WHERE station_city = %s"
    cursor.execute(query, (stad,))
    #haalt de resultaten op
    city_installments = cursor.fetchall()
    #initaliseert de x-coordinaat voor het plaatsen van afbeelddingen.
    initial_x = 530
    #controleert of er instalaties zijn en plaatst de bijbehorende afbeeldingen
    if city_installments[0][2]:
        initial_x += 150
        canvas.create_image(initial_x, foto_y_coordinaten + 130, image=image_ovfiets)

    if city_installments[0][3]:
        initial_x += 150
        canvas.create_image(initial_x, foto_y_coordinaten + 130, image=image_lift)

    if city_installments[0][4]:
        initial_x += 150
        canvas.create_image(initial_x, foto_y_coordinaten + 130, image=image_toilet)

    if city_installments[0][5]:
        initial_x += 150
        canvas.create_image(initial_x, foto_y_coordinaten + 130, image=image_pr)

    return city_installments
def haal_recente_berichten():
    cursor = conn.cursor()
    #weer een sql query uit om de 5 meest recente berichten opt e halen met een max van 5
    cursor.execute('SELECT * FROM ZUIL order by DATUM DESC LIMIT 5')
    recente_berichten = cursor.fetchall()
    #geeft variabelen aand e coordinaten
    berichten = ""
    y_coordinate = 10
    y_coordinate_text = 155

    for i in recente_berichten:
       bericht = i[2]
       # splitst het bericht in delen na elke 30 karachters waardoor het bericht netjes onde relkaar komt te staan
       max_length = 30
       gesplit_bericht = "\n".join([bericht[i:i + max_length] for i in range(0, len(bericht), max_length)])
    #maakt tesktt op het venster met details van het bericht
       canvas.create_text(300, y_coordinate_text, text=f"Naam: {i[0]} \n Station: {i[1]} \n bericht:{gesplit_bericht} \n datum: {i[3]}\n", fill="black", font=("Calibri", 15, "bold"))
       instalaties(i[1], y_coordinate)
       y_coordinate += 140
       y_coordinate_text += 135
    return berichten
#functie voor de text bestand
def text():
    #roept de functie op en zet hem in het variable resultaat.
    resultaten = haal_recente_berichten()
    #maakt een tekst op de vcanvas met de recente berichten
    canvas.create_text(410, 400, text=resultaten, fill="black", font=("Calibri", 25, "bold"))

text()

getoonde_stations = set()





root.mainloop()