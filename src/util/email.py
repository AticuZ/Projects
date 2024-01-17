import mysql.connector as _connector
import smtplib as _smt
import time as _time
import threading as _threading
import schedule as _schedule
import datetime as _datetime

from email.message import EmailMessage


def email_schedule():
    print("start schedule")
    #schedule.every(5).seconds.do(send_email_schedule)
    _schedule.every().day.at("00:00").do(send_email_schedule)
    while True:
        _schedule.run_pending()
        _time.sleep(1)


def send_email_schedule():

    query = ("SELECT user.Email FROM user INNER JOIN ticket WHERE user.UID = ticket.UID AND DATE_ADD(DATE(ticket.DepartureTime), INTERVAL -2 DAY) LIKE CURDATE()")

    cnx = _connector.connect(
        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
    cursor = cnx.cursor()

    cursor.execute(query)

    Email_Address = cursor.fetchall()

    cursor.close()
    cnx.close()


    for address in Email_Address:

        msg = EmailMessage()
        msg['Subject'] = "CheckIn " + str(_datetime.now())
        msg['to'] = [address[0]]

        msg.set_content(
            """Dear Customer, The flight you have booked departs the day after tomorrow. Online Check-In will be available 24 hours before departure. We wish you a pleasant journey with DataAirlines.""")
        sender = 'DBSoSeGroupFEmployee@gmx.de'
        password = 'Database2020Employee1'
        msg['From'] = sender
        with _smt.smtplib.SMTP('mail.gmx.net', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(sender, password)

            smtp.send_message(msg)


## start email event ##
thread = _threading.Thread(target=email_schedule)
thread.start()


def send_email(email_Address, UID, FCName, DepartureTime, Miles, Seat, Luggage, SeatType, Price):
    msg = EmailMessage()
    msg['Subject'] = "Booking Conformation " + str(_time.datetime.now())
    msg['to'] = ["siegbertschnoesel9@gmail.com"]


    if SeatType == "E":
        SeatType = "Economy"
    elif SeatType == "B":
        SeatType = "Business"
    elif SeatType == "F":
        SeatType = "First Class"

    msg.set_content(
        f"""Dear Customer,
        Thank you for choosing to travel with DataAirlines. Your Flight Details are 
        Username: {UID}
        Flightcode: {FCName}
        DepartureTime: {DepartureTime}
        Miles: {Miles}
        Seat Number: {Seat}
        Luggage: {Luggage}kg
        Seat Class: {SeatType}
        Price: {Price}€ """)
    sender = 'DBSoSeGroupFEmployee@gmx.de'
    password = 'Database2020Employee1'
    msg['From'] = sender
    with _smt.smtplib.SMTP('mail.gmx.net', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(sender, password)

        smtp.send_message(msg)