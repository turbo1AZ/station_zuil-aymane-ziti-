import datetime
import random
import csv

#wat hier gebeurt is dat de gerbuiker eenn bericht en naam kan in vullen. waneer deze zijn ingevuld wordt er onder met if state ments gecontroleert of ze de juiste eigen schappen hebben die geraagd word.
while True:
    woord = input ('schrijf een bericht van max 140 karakters: ')
    naam = input('wat is je naam?:')
    ###### Naam ######
    if len(naam) == 0:
        naam - 'anoniem'

    naam1 = ('Naam: ' + naam)

    print(naam1)

    ##### Bericht ######
    if len(woord) <= 140:
        bericht1 = ('Bericht: ' + woord)
        print(bericht1)
    else:
        print('tekst is te lang schrijf een kortere bericht')

    ######### Datum & Tijd ##########
    now = datetime.datetime.now()

    datum = now.strftime('%Y-%m-%d %H:%M')
    print(datum)

    ############# Station_keuze ###############
    station = ['Den Bosch', 'Utrecht', 'Oss']
    gekozen_station = random.choice(station)
    station1 =(f'station: {gekozen_station}\n')
    print(station1)

    #################### Bestand open ########################
    with (open("stations_zuil.csv", "a", newline="") as bestand):

        # Maak een writer-object.
        writer = csv.DictWriter(bestand, fieldnames=['naam', 'bericht', 'station', 'datum', ])  # dot schrijft

        # Schrijf een rij naar het bestand.
        writer.writerow({
            'naam': naam,
            'bericht': woord,
            'station': gekozen_station,
            'datum': datum,

        })
    # Sluit het bestand.
    bestand.close()


