import csv

import psycopg2
import datetime

#maakt een verbinding met  de postgreSQL-database:

conn = psycopg2.connect(
    host='172.166.133.82',
    database='station_zuil',
    user='postgres',
    password='aymane21',
    port='5432')

#creeert een lege lijst om de gegevens uit het csv bestand in op te slaan
bestand1 = []


bestandjee = 'stations_zuil.csv'

#opent het csv bestand en leest de inhoud. voor elke rij in het bestand maakt hij een rij in bestand1
with open(bestandjee, 'r') as csv_bestand:
    lezer = csv.reader(csv_bestand)
    for rij in lezer:
        bestand1.append(rij)

#vraagt de naam en email adres vand e gebruiker in te vullen en zet er de datum en tijd bij
naam = input('Naam van de moderator: ')
email = input('E-mailadres van de moderator: ')


tijd = datetime.datetime.now()
datum = tijd.strftime('%Y-%m-%d %H:%M')
print(datum, 'naam:', naam, 'email:', email)

try:#maakt een lege lijst en een database cursor.
    cursor = conn.cursor()
    rij1 = []
#haal reiziger , bericht en station uit de rij
    for rij in bestand1:
        reiziger = rij[0]
        bericht = rij[1]
        station = rij[2]

            #toont reiziger bericht en station, vraagt of het nog moet worden goedgekeurd.
        print(f'Reiziger: {reiziger}\nBericht: {bericht}\nStation: {station}')
        beoordeling = input('Goedkeuren? Type ja of nee in: ')
            #als het ja is dan ihet goed gekeurd
        if beoordeling == 'ja':
            beoordeling = True
            print('Bericht is goedgekeurd')

            #voert een sql query uit om de gegevens ind e database  in te voerren inclusief de naam van de modertor en email.
            query = """
                INSERT INTO zuil (reiziger, bericht, station, datum, beoordeling, datum_beoordeling, naam_moderator, email_mod)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (reiziger, bericht, station, datum, beoordeling, datum, naam, email))
            conn.commit()
            #als het is af gekeurd dan wordt het print hij dat uit en wordt het uit de csv bestand verwijderd.
        else:
            print('Bericht is afgekeurd')


#opent het csv bestand en zorgt dat de rijen er uit worden verwijderd.
    with open(bestandjee, 'w', newline='') as csv_bestand:
        schrijft = csv.writer(csv_bestand)
        schrijft.writerows(rij1)

#sluit de verbinding met post gresql
finally:
    conn.close()