import bcrypt as _bcrypt
import mysql.connector as _connector
import time as _time

from flask import Flask, render_template, url_for, redirect, request, session, flash

import util.email as _email

app = Flask(__name__)
app.secret_key = "qwertz"


def pwCheck(UID, pw, employee):
    if employee == "on":

        cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                      database='flightproject')

        cursor = cnx.cursor()
        query = (
            'SELECT password FROM User WHERE UID = %s AND isEmployee = 1')
        data = (UID,)

        cursor.execute(query, data)
        account = cursor.fetchone()

        cursor.close()
        cnx.close()
        
        if not account:
            return False

        hashed = account[0].encode()
        pwencoded = pw.encode()

        if _bcrypt.checkpw(pwencoded, hashed):
            return True
        else:
            return False
    else:
        
        query = ('SELECT password FROM User WHERE UID = %s')
        data = (UID,)

        cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                      database='flightproject')

        cursor = cnx.cursor()

        cursor.execute(query, data)
        account = cursor.fetchone()

        cursor.close()
        cnx.close()

        if not account:
            return False

        hashed = account[0].encode()
        pwencoded = pw.encode()

        if _bcrypt.checkpw(pwencoded, hashed):
            return True
        else:
            return False


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':

        UID = request.form['UID']
        pw = request.form['password']
        employee = request.form['emp']

        if pwCheck(UID, pw, employee):
            session["user"] = UID
            #session["pw"] = pw
            session["emp"] = employee

            query = ("SELECT Tier FROM User WHERE UID = %s")
            data = (UID,)

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')

            cursor = cnx.cursor()
            cursor.execute(query, data)
            tier = cursor.fetchall()
            cursor.close()

            session["tier"] = tier[0][0]

            if session["emp"] == "on":
                return render_template('emp_home.html')
            else:
                return render_template('home.html')
        else:
            flash("Your Username or password is wrong.", "info")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            if session["emp"] == "on":
                return render_template('emp_home.html')
            else:
                return render_template('home.html')
        else:
            return redirect(url_for("login"))


@app.route('/tiers', methods=['GET', 'POST'])
def tiers():
    if "user" in session:
        if session["emp"] == "on":
            if request.method == 'POST':

                details = request.form
                b_PriceMult = details['bPriceMult']
                b_LuggageMult = details['bLuggageMult']
                b_MilesMult = details['bMilesMult']
                b_SeatUpgrade = details['bSeatUpgrade']
                b_ReservationTime = details['bReservationTime']

                s_PriceMult = details['sPriceMult']
                s_LuggageMult = details['sLuggageMult']
                s_MilesMult = details['sMilesMult']
                s_SeatUpgrade = details['sSeatUpgrade']
                s_ReservationTime = details['sReservationTime']

                g_PriceMult = details['gPriceMult']
                g_LuggageMult = details['gLuggageMult']
                g_MilesMult = details['gMilesMult']
                g_SeatUpgrade = details['gSeatUpgrade']
                g_ReservationTime = details['gReservationTime']

                query_b = (
                    "UPDATE tier SET PriceMult = %s, LuggageMult = %s , MilesMult = %s, SeatUpgrade=%s , ReservationTime = %s   WHERE Tier ='b'")
                query_s = (
                    "UPDATE tier SET PriceMult = %s, LuggageMult = %s , MilesMult = %s, SeatUpgrade=%s , ReservationTime = %s   WHERE Tier = 's'")
                query_g = (
                    "UPDATE tier SET PriceMult = %s, LuggageMult = %s , MilesMult = %s, SeatUpgrade=%s , ReservationTime = %s   WHERE Tier = 'g'")

                data_b = (b_PriceMult, b_LuggageMult, b_MilesMult,
                          b_SeatUpgrade, b_ReservationTime,)
                data_s = (s_PriceMult, s_LuggageMult, s_MilesMult,
                          s_SeatUpgrade, s_ReservationTime,)
                data_g = (g_PriceMult, g_LuggageMult, g_MilesMult,
                          g_SeatUpgrade, g_ReservationTime,)

                cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                              database='flightproject')

                cursor = cnx.cursor()
                
                try:
                    cursor.execute(query_b, data_b)
                    cursor.execute(query_s, data_s)
                    cursor.execute(query_g, data_g)
                except Exception:
                    flash("Something went wrong")
                    return redirect(url_for("tiers"))

                cnx.commit()

                cursor.close()
                cnx.close()

                query = ('SELECT * FROM tier ORDER BY MilesMult;')

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query)

                tiers = cursor.fetchall()

                cursor.close()
                cnx.close()

                return render_template('emp_tiers.html', tiersContent=tiers, userTier=session["tier"] )

            else:
                query = ('SELECT * FROM tier ORDER BY MilesMult;')

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query)

                tiers = cursor.fetchall()

                cursor.close()
                cnx.close()

                return render_template('emp_tiers.html', tiersContent=tiers , userTier=session["tier"])
        else:
            query = ('SELECT * FROM tier ORDER BY MilesMult;')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            tiers = cursor.fetchall()

            cursor.close()
            cnx.close()

            return render_template('tiers.html', tiersContent=tiers , userTier=session["tier"])
    else:
        return redirect(url_for("login"))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if "user" in session:
        if session["emp"] == "on":
            return render_template('emp_home.html')
        else:
            return render_template('home.html')
    else:
        return render_template('signup.html')


@app.route('/signupcheck', methods=['GET', 'POST'])
def signupckeck():
    if request.method == "POST":
        if "user" in session:
            if session["emp"] == "on":
                return render_template('emp_home.html')
            else:
                return render_template('home.html')
        else:
            details = request.form
            User_UID = details['inputUID']
            User_Password = details['inputPassword']
            User_firstName = details['inputFirstName']
            User_lastName = details['inputLastName']
            User_email = details['inputEmail']
            User_tel = details['inputTel']
            User_address = details['inputAddress']
            User_Birthday = details['inputBirthday']
            User_IBAN = details['inputIBAN']

            passwordtest = User_Password.encode()

            hashed = _bcrypt.hashpw(passwordtest, _bcrypt.gensalt())

            User_Password = hashed.decode()

            query_search = ('SELECT UID FROM User WHERE UID = %s')
            data_search = (User_UID,)

            query_insert = (
                "INSERT INTO User(UID, Password, firstName, lastName, email, tel, address, Birthday, IBAN) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data_insert = (User_UID, User_Password, User_firstName, User_lastName,
                            User_email, User_tel, User_address,User_Birthday, User_IBAN)

            cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                          database='flightproject')

            cursor = cnx.cursor()

            cursor.execute(query_search, data_search)

            result = cursor.fetchone()
            if result:
                flash("Your UserName is taken")
                return redirect(url_for("signup"))

            try:
                cursor.execute(query_insert, data_insert)
            except Exception:
                flash("Something went wrong. Please check your data.")
                return redirect(url_for("signup"))
                
            cnx.commit()

            cursor.close()
            cnx.close()

            flash("Your signup was successful")
            return redirect(url_for("login"))
    else:
        return redirect(url_for("signup"))


@app.route('/empsignup', methods=['GET', 'POST'])
def empsignup():
    if "user" in session:
        if session["emp"] == "on":
            if request.method == 'POST':

                details = request.form
                User_UID = details['inputUID']
                User_Password = details['inputPassword']
                User_firstName = details['inputFirstName']
                User_lastName = details['inputLastName']
                User_email = details['inputEmail']
                User_tel = details['inputTel']
                User_address = details['inputAddress']
                User_Birthday = details['inputBirthday']
                User_IBAN = details['inputIBAN']
                User_Wage = details['inputWage']

                passwordtest = User_Password.encode()

                hashed = _bcrypt.hashpw(passwordtest, _bcrypt.gensalt())

                User_Password = hashed.decode()

                query_insert = (
                    "INSERT INTO User(UID, Password, firstName, lastName, email, tel, address, Birthday, IBAN, Wage, isEmployee) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)")
                data_insert = (User_UID, User_Password, User_firstName, User_lastName,
                               User_email, User_tel, User_address,User_Birthday, User_IBAN, User_Wage)

                query_search = (
                    'SELECT UID FROM User WHERE UID = %s and isEmployee = 1')
                data_search = (User_UID,)

                cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                              database='flightproject')

                cursor = cnx.cursor()

                cursor.execute(query_search, data_search)

                result = cursor.fetchone()
                if result:
                    flash("This employee already exists")
                    return redirect(url_for("emp_signup.html"))

                try:
                    cursor.execute(query_insert, data_insert)
                except Exception:
                    flash("Something went wrong. Please check your data.")
                    return redirect(url_for("empsignup"))

                cnx.commit()

                cursor.close()
                cnx.close()

                flash("The employee has been inserted!", "info")

                return render_template('emp_signup.html')

            else:
                return render_template('emp_signup.html')
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/aircrafts', methods=['GET', 'POST'])
def aircrafts():
    if "user" in session:
        if session["emp"] == "on":

            query = ('SELECT DISTINCT ACName FROM aircraft  ')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsAircraft = cursor.fetchall()

            cursor.close()
            cnx.close()    
            
            if request.method == 'POST':
                if request.form["Search"] == "Search":
                    MinCapacity = 0
                    if request.form["MinCapacity"]:
                        MinCapacity = request.form["MinCapacity"]

                    MaxCapacity = 10000000000000000
                    if request.form["MaxCapacity"]:
                        MaxCapacity = request.form["MaxCapacity"]
                        
                    ACName = "%"
                    if request.form["Aircraft"]:
                        ACName = request.form["Aircraft"]

                    query = ('SELECT * FROM aircraft WHERE ACName LIKE %s AND MaxLuggage >= %s AND MaxLuggage <= %s')
                    data = (ACName, MinCapacity, MaxCapacity,)

                    cnx = _connector.connect(
                        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                    cursor = cnx.cursor()

                    cursor.execute(query,data)

                    aircrafts = cursor.fetchall()

                    cursor.close()
                    cnx.close()

                    return render_template('emp_aircrafts.html', aircraftList=aircrafts, SearchOptionsAircraft = SearchOptionsAircraft)

                else:
                    aircraft = request.form
                    ACName = aircraft['ACName']
                    Seats_E = aircraft['Seats_E']
                    Seats_B = aircraft['Seats_B']
                    Seats_F = aircraft['Seats_F']
                    Luggage_E = aircraft['Luggage_E']
                    Luggage_B = aircraft['Luggage_B']
                    Luggage_F = aircraft['Luggage_F']
                    MaxLuggage = aircraft['MaxLuggage']

                    query_update = (
                        "REPLACE INTO aircraft(ACName, Seats_E, Seats_B, Seats_F, Luggage_E, Luggage_B, Luggage_F, MaxLuggage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
                    data_update = (ACName, Seats_E, Seats_B, Seats_F,
                                Luggage_E, Luggage_B, Luggage_F, MaxLuggage)

                    cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                                database='flightproject')

                    cursor = cnx.cursor()

                    try:
                        cursor.execute(query_update, data_update)
                    except Exception:
                        flash("Something went wrong")
                        return redirect(url_for("aircrafts"))

                    cnx.commit()

                    cursor.close()
                    cnx.close()

                    flash("The Aircraft has been updated/inserted!", "info")

                    return redirect(url_for("aircrafts"))

            else:
                query = ('SELECT * FROM aircraft')

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query)

                aircrafts = cursor.fetchall()

                cursor.close()
                cnx.close()

                return render_template('emp_aircrafts.html', aircraftList=aircrafts, SearchOptionsAircraft = SearchOptionsAircraft)
        else:
            return render_template('home')
    else:
        return redirect(url_for("login"))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if "user" in session:
        if session["emp"] == "on":
            if request.method == 'POST':
                
                profile = request.form
                UID = profile['inputUID']
                FirstName = profile['inputFirstName']
                LastName = profile['inputLastName']
                Birthday = profile['inputBirthday']
                Email = profile['inputEmail']
                Tel = profile['inputTel']
                Address = profile['inputAddress']
                IBAN = profile['inputIBAN']


                if not pwCheck(UID, request.form['OldPassword'], session['emp']):
                    flash("Please enter your current Password to update your profile")
                    return redirect(url_for("profile"))

                if request.form["inputPassword"]:
                    USER_Password = request.form["inputPassword"]

                    passwordtest = User_Password.encode()
                    hashed = _bcrypt.hashpw(passwordtest, _bcrypt.gensalt())
                    User_Password = hashed.decode()
                    query_update = (
                        "UPDATE User SET FirstName = %s, LastName = %s, Birthday = %s, Email = %s, Tel = %s, Address = %s, IBAN = %s, Password = %s WHERE UID = %s")
                    data_update = (FirstName, LastName, Birthday, Email, Tel, Address, IBAN, UID, User_Password,)
                else:
                    query_update = (
                        "UPDATE User SET FirstName = %s, LastName = %s, Birthday = %s, Email = %s, Tel = %s, Address = %s, IBAN = %s WHERE UID = %s")
                    data_update = (FirstName, LastName, Birthday, Email, Tel, Address, IBAN, UID,)
               
                cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                              database='flightproject')

                cursor = cnx.cursor()

                cursor.execute(query_update, data_update)

                cnx.commit()

                cursor.close()
                cnx.close()

                flash("Userdata has been updated.", "info")

                return redirect(url_for("profile"))
                
            else:
                query = ('SELECT UID, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, Wage FROM user')

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query)

                UserData = cursor.fetchall()

                cursor.close()
                cnx.close()

                return render_template('emp_profile.html', UserData=UserData)
        else:
            if request.method == 'POST':
  
                profile = request.form
                UID = profile['inputUID']
                FirstName = profile['inputFirstName']
                LastName = profile['inputLastName']
                Birthday = profile['inputBirthday']
                Email = profile['inputEmail']
                Tel = profile['inputTel']
                Address = profile['inputAddress']
                IBAN = profile['inputIBAN']


                if not pwCheck(UID, request.form['OldPassword'], session['emp']):
                    flash("Please enter your current Password to update your profile")
                    return redirect(url_for("profile"))

                if request.form["inputPassword"]:
                    User_Password = request.form["inputPassword"]
                    print(User_Password)
                    passwordtest = User_Password.encode()
                    hashed = _bcrypt.hashpw(passwordtest, _bcrypt.gensalt())
                    User_Password = hashed.decode()
                    query_update = (
                        "UPDATE User SET Password = %s, FirstName = %s, LastName = %s, Birthday = %s, Email = %s, Tel = %s, Address = %s, IBAN = %s WHERE UID = %s")
                    data_update = (User_Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, UID, )
                else:
                    query_update = (
                        "UPDATE User SET FirstName = %s, LastName = %s, Birthday = %s, Email = %s, Tel = %s, Address = %s, IBAN = %s WHERE UID = %s")
                    data_update = (FirstName, LastName, Birthday, Email, Tel, Address, IBAN, UID,)
               
                cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                              database='flightproject')

                cursor = cnx.cursor()

                cursor.execute(query_update, data_update)

                cnx.commit()

                cursor.close()
                cnx.close()

                flash("Userdata has been updated.", "info")

                return redirect(url_for("profile"))
                
            else:
                query = ('SELECT UID, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier FROM user WHERE UID = %s')
                data = (session["user"],)
                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query,data)

                UserData = cursor.fetchone()

                cursor.close()
                cnx.close()

                return render_template('profile.html', UserData = UserData)

    else:
        return redirect(url_for("login"))


@app.route('/specialoffer=<OID>', methods=['GET', 'POST'])
def specialofferDisplay(OID):
    if request.method == "POST":
        if "user" in session:
            if session["emp"] == "on":
                return redirect(url_for("home"))
            else:
                # ------------------------------ Get available Flights------------------------------------------

                #FCName = request.form["FCName"]

                #query_E = (
                    #'SELECT CAST(DepartureTime AS char) FROM flight INNER JOIN flightcode ON flight.FCID LIKE flightcode.FCID WHERE FCName = %s AND FreeSeat_E > 0 AND DepartureTime > NOW();')

                #query_B = (
                    #'SELECT CAST(DepartureTime AS char) FROM flight INNER JOIN flightcode ON flight.FCID LIKE flightcode.FCID WHERE FCName = %s AND FreeSeat_B > 0 AND DepartureTime > NOW();')

                #query_F = (
                    #'SELECT CAST(DepartureTime AS char) FROM flight INNER JOIN flightcode ON flight.FCID LIKE flightcode.FCID WHERE FCName = %s AND FreeSeat_F > 0 AND DepartureTime > NOW();')

                FCID = request.form["FCID"]

                query_E = (
                    'SELECT CAST(DepartureTime AS char) FROM flight WHERE FCID = %s AND FreeSeat_E > 0 AND DepartureTime > NOW()')

                query_B = (
                    'SELECT CAST(DepartureTime AS char) FROM flight WHERE FCID = %s AND FreeSeat_B > 0 AND DepartureTime > NOW()')

                query_F = (
                    'SELECT CAST(DepartureTime AS char) FROM flight WHERE FCID = %s AND FreeSeat_F > 0 AND DepartureTime > NOW()')

                data = (FCID,)

                data = (FCID,)

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')

                cursor = cnx.cursor()
                cursor.execute(query_E, data)
                flights_economy = cursor.fetchall()
                cursor.close()

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')

                cursor = cnx.cursor()
                cursor.execute(query_B, data)
                flights_business = cursor.fetchall()
                cursor.close()

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')

                cursor = cnx.cursor()
                cursor.execute(query_F, data)
                flights_firstclass = cursor.fetchall()
                cursor.close()

                cnx.close()

                # ------------------------------ Get Prices for Flights------------------------------------------

                OfferPriceMult = request.form["OfferPriceMult"]
                OfferLuggageMult = request.form["OfferLuggageMult"]
                OfferMilesMult = request.form["OfferMilesMult"]
                SeatUpgrade = request.form["SeatUpgrade"]

                query_conditions = ("SELECT FLOOR(Price_E * PriceMult * %s) as Price_E,FLOOR(Luggage_E * LuggageMult * %s) as Luggage_E,FLOOR(Miles_E * MilesMult * %s) as Miles_E, FLOOR(Price_B * PriceMult * %s) as Price_B,FLOOR(Luggage_B * LuggageMult * %s) as Luggage_B,FLOOR(Miles_B * MilesMult * %s) as Miles_B, FLOOR(Price_F * PriceMult * %s) as Price_F,FLOOR(Luggage_F * LuggageMult * %s) as Luggage_F,FLOOR(Miles_F * MilesMult * %s) as Miles_F FROM tier, flightcode INNER JOIN aircraft ON flightcode.ACID = aircraft.ACID WHERE flightcode.FCID = %s and tier.tier = %s")

                data_conditions = (OfferPriceMult, OfferLuggageMult, OfferMilesMult, OfferPriceMult, OfferLuggageMult,
                                   OfferMilesMult, OfferPriceMult, OfferLuggageMult, OfferMilesMult, FCID, session["tier"],)

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')

                cursor = cnx.cursor()
                cursor.execute(query_conditions, data_conditions)
                flights_conditions = cursor.fetchall()[0]
                cursor.close()

                cnx.close()

                return render_template("specialofferDisplay.html", FCID=FCID, flights_economy=flights_economy, flights_business=flights_business, flights_firstclass=flights_firstclass, flightcode_details=flights_conditions, SeatUpgrade = SeatUpgrade)
        else:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("home"))


@app.route('/specialoffers', methods=['GET', 'POST'])
def specialoffers():
    if "user" in session:
        if session["emp"] == "on":

            ## Search Options ##
            query = ('SELECT DISTINCT FCName FROM flightcode ')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsFCID = cursor.fetchall()

            cursor.close()
            cnx.close()

            query = ('SELECT DISTINCT OName FROM specialoffer ')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsOID = cursor.fetchall()

            cursor.close()
            cnx.close()

            if request.method == 'POST':
                if request.form["Search"] == "Search":

                    ## Search Bar Variables ##
                    FCName = "%"
                    if request.form["FCID"]:
                        FCName = request.form["FCID"]
                    OID = "%"
                    if request.form["OID"]:
                        OID = request.form["OID"]
                    Status = "%"
                    if request.form["status"] != "all":
                        Status = request.form["status"]


                    query = ('SELECT specialoffer.FCID, FCName, OName, PriceMult, LuggageMult, MilesMult, SeatUpgrade, ReservationTime, Status FROM specialoffer INNER JOIN flightcode ON specialoffer.FCID LIKE flightcode.FCID WHERE FCName LIKE %s AND OName LIKE %s AND Status LIKE %s')
                    data = (FCName, OID, Status)

                    cnx = _connector.connect(
                        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                    cursor = cnx.cursor()

                    cursor.execute(query, data)

                    specialOffers = cursor.fetchall()

                    cursor.close()
                    cnx.close()

                    return render_template('emp_specialoffers.html', specialOfferList = specialOffers, SearchOptionsOID = SearchOptionsOID, SearchOptionsFCID = SearchOptionsFCID)
                else:

                    ## On Insert ##
                    specialOffer = request.form
                    FCID = specialOffer['FCID']
                    if FCID == "":
                        FCID = None
                    FCName = specialOffer['FCName']
                    OName = specialOffer['OName']
                    PriceMult = specialOffer['PriceMult']
                    LuggageMult = specialOffer['LuggageMult']
                    MilesMult = specialOffer['MilesMult']
                    SeatUpgrade = specialOffer['SeatUpgrade']
                    ReservationTime = specialOffer['ReservationTime']
                    Status = specialOffer['Status']

                    query_update = (
                        "INSERT INTO specialoffer(FCID, OName, PriceMult, LuggageMult, MilesMult, SeatUpgrade, ReservationTime, Status) VALUES ((SELECT FCID FROM flightcode WHERE %s LIKE flightcode.FCName), %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE FCID = (SELECT FCID FROM flightcode WHERE %s LIKE flightcode.FCName), OName = %s, PriceMult = %s, LuggageMult = %s, MilesMult = %s, SeatUpgrade = %s, ReservationTime = %s, Status = %s")
                    data_update = (FCName, OName, PriceMult, LuggageMult,
                                MilesMult, SeatUpgrade, ReservationTime, Status,FCName, OName, PriceMult, LuggageMult,
                                MilesMult, SeatUpgrade, ReservationTime, Status)

                    cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                                database='flightproject')

                    cursor = cnx.cursor()

                    #try:
                    cursor.execute(query_update, data_update)
                   # except Exception:
                        #flash("Something went wrong")
                        #return redirect(url_for("specialoffers"))

                    cnx.commit()

                    cursor.close()
                    cnx.close()


                    flash("The SpecialOffer has been updated/inserted!", "info")
                    return redirect(url_for("specialoffers"))

            else:
                query = (
                    'SELECT specialoffer.FCID, FCName, OName, PriceMult, LuggageMult, MilesMult, SeatUpgrade, ReservationTime, Status FROM specialoffer INNER JOIN flightcode ON specialoffer.FCID LIKE flightcode.FCID')

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query)

                specialOffers = cursor.fetchall()

                cursor.close()
                cnx.close()

                return render_template('emp_specialoffers.html', specialOfferList = specialOffers, SearchOptionsOID = SearchOptionsOID, SearchOptionsFCID = SearchOptionsFCID)
        else:

            ## Search Options ##
            query = ('SELECT DISTINCT PortName FROM flightcode INNER JOIN Airport ON flightcode.DepartureAirport = airport.APID')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsFROM = cursor.fetchall()

            cursor.close()
            cnx.close()

            query = ('SELECT DISTINCT PortName FROM flightcode INNER JOIN Airport ON flightcode.ArrivalAirport = airport.APID')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsTO = cursor.fetchall()

            cursor.close()
            cnx.close()

            ## Tiers Mult für den Price Display ##
            query_conditions = (
                "SELECT PriceMult FROM Tier WHERE tier.tier = %s")

            data_conditions = (session["tier"],)

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')

            cursor = cnx.cursor()
            cursor.execute(query_conditions, data_conditions)
            X = cursor.fetchall()
            cursor.close()

            cnx.close()

            TierPriceMult = X[0][0]

            if request.method == 'POST':

                ## Search Bar Variables ##
                if request.form["Search"] == "Search":

                    minPrice = 0
                    if request.form["MinPrice"]:
                        minPrice = request.form["MinPrice"]
                    MaxPrice = 10000000000000000
                    if request.form["MaxPrice"]:
                        MaxPrice = request.form["MaxPrice"]
                    MinTime = "00:00:00"
                    if request.form["MinTime"]:
                        MinTime = request.form["MinTime"]
                    MaxTime = "23:59:59"
                    if request.form["MaxTime"]:
                        MaxTime = request.form["MaxTime"]
                    From = "%"
                    if request.form["From"]:
                        From = request.form["From"]
                    To = "%"
                    if request.form["To"]:
                        To = request.form["To"]


                    query = ("""SELECT Portname , ArrivAirport, FLOOR(Price_E*PriceMult * %s), ScheduledDepartureTime, FlightDuration , DayWeek, OID, PriceMult, LuggageMult, MilesMult, test.FCID FROM 
                                (SELECT * FROM ((SELECT Portname , Price_E, ScheduledDepartureTime, FlightDuration , DayWeek, FCID as FCIDold
			                    FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
			                    WHERE Portname LIKE %s) as Departure
		                        INNER JOIN 
			                    (SELECT Portname as ArrivAirport, FCID
			                    FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
			                    WHERE Portname LIKE %s) as Arrival 
		                        ON Departure.FCIDold = Arrival.FCID)) as test
                                NATURAL JOIN
                                (SELECT * FROM offerto NATURAL JOIN specialoffer WHERE UID = %s AND status = 1) as ActiveOffers 
                                WHERE UID = %s AND FLOOR(Price_E*PriceMult * %s) >= %s AND FLOOR(Price_E*PriceMult * %s) <= %s AND ScheduledDepartureTime >= %s AND ScheduledDepartureTime <= %s""")
                    
                    data = (TierPriceMult, From, To, session["user"], session["user"],TierPriceMult, minPrice,TierPriceMult, MaxPrice, MinTime,
                            MaxTime, )

                    cnx = _connector.connect(
                        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                    cursor = cnx.cursor()

                    cursor.execute(query, data)

                    specialoffers = cursor.fetchall()

                    cursor.close()
                    cnx.close()

                    return render_template('specialoffers.html', specialoffers=specialoffers, UID=session["user"], SearchOptionsFROM = SearchOptionsFROM, SearchOptionsTO = SearchOptionsTO)
            else:

                ## Display Specialoffers ##
                query = ("""SELECT Portname , ArrivAirport, FLOOR(Price_E*PriceMult * %s), ScheduledDepartureTime, FlightDuration , DayWeek, OID, PriceMult, LuggageMult, MilesMult, test.FCID FROM 
                                (SELECT * FROM ((SELECT Portname , Price_E, ScheduledDepartureTime, FlightDuration , DayWeek, FCID as FCIDold
			                    FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
			                    WHERE Portname LIKE "%") as Departure
		                        INNER JOIN 
			                    (SELECT Portname as ArrivAirport, FCID
			                    FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
			                    WHERE Portname LIKE "%") as Arrival 
		                        ON Departure.FCIDold = Arrival.FCID)) as test
                                NATURAL JOIN
                                (SELECT * FROM offerto NATURAL JOIN specialoffer WHERE UID = %s AND status = 1) as ActiveOffers """)
                data = (TierPriceMult, session["user"], )

                cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                            database='flightproject')

                cursor = cnx.cursor()

                cursor.execute(query, data)

                specialoffers = cursor.fetchall()

                cnx.commit()

                cursor.close()
                cnx.close()

                return render_template('specialoffers.html', specialoffers=specialoffers, SearchOptionsFROM = SearchOptionsFROM, SearchOptionsTO = SearchOptionsTO)
    else:
        return redirect(url_for("login"))


@app.route('/specialoffersto', methods=['GET', 'POST'])
def specialoffersto():
    if "user" in session:          
        if session["emp"] == "on":

            ## Search Options ##
            query = ('SELECT DISTINCT FCName , OName, OID, FCID FROM flightcode NATURAL JOIN Specialoffer ')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SpecialOfferOptions = cursor.fetchall()

            cursor.close()
            cnx.close()

            if request.method == 'POST':

                details = request.form

                x = details['SpecialOffer'].split()


                FCName = x[0]
                OName = x[2]
                for i in range(3,len(x)): 
                    OName =  OName +  " " + x[i]


                if details['To'] == "User":
                    UID = details['UID']

                    query_insert = (
                        "REPLACE INTO offerto(FCID, OID, UID) VALUES ((SELECT FCID FROM flightcode WHERE FCName LIKE %s), (SELECT OID FROM specialoffer WHERE OName LIKE %s), %s)")
                    data_insert = (FCName, OName, UID)

                    print(data_insert)

                    cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                                  database='flightproject')

                    cursor = cnx.cursor()
                    
                    try:
                        cursor.execute(query_insert, data_insert)
                    except Exception:
                        flash("Something went wrong")
                        return redirect(url_for("specialoffersto"))
                    cnx.commit()

                    cursor.close()
                    cnx.close()

                else:
                    Tier = details['Tier']

                    query_insert = (
                        "REPLACE INTO offerto SELECT * FROM (SELECT FCID,OID FROM specialoffer WHERE FCID LIKE (SELECT FCID FROM flightcode WHERE FCName LIKE %s) AND OID LIKE (SELECT OID FROM specialoffer WHERE OName LIKE %s)) AS Tiers JOIN (SELECT UID FROM User WHERE Tier = %s) AS UIDs ;")
                    data_insert = (FCName, OName, Tier)

                    cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                                  database='flightproject')

                    cursor = cnx.cursor()
                    
                    try:
                        cursor.execute(query_insert, data_insert)
                    except Exception:
                        flash("Something went wrong")
                        return redirect(url_for("specialoffersto"))
                    cnx.commit()

                    cursor.close()
                    cnx.close()

                flash("The Offer has been send!")
                return render_template('emp_specialoffersto.html', SpecialOfferOptions = SpecialOfferOptions)
            else:
                return render_template('emp_specialoffersto.html', SpecialOfferOptions = SpecialOfferOptions)
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/flightcodes', methods=['GET', 'POST'])
def flightcodes():
    if "user" in session:
        if session["emp"] == "on":

            query = ('SELECT DISTINCT PortName FROM flightcode INNER JOIN Airport ON flightcode.DepartureAirport = airport.APID')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsFROM = cursor.fetchall()

            cursor.close()
            cnx.close()

            query = ('SELECT DISTINCT PortName FROM flightcode INNER JOIN Airport ON flightcode.ArrivalAirport = airport.APID')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsTO = cursor.fetchall()

            cursor.close()
            cnx.close()

            query = ('SELECT DISTINCT FCName FROM flightcode ')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsFlightcode = cursor.fetchall()

            cursor.close()
            cnx.close()

            query = ('SELECT DISTINCT ACName FROM aircraft  ')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsAircraft = cursor.fetchall()

            cursor.close()
            cnx.close()

            if request.method == 'POST':
                if request.form["Search"] == "Search":

                    minPrice = 0
                    if request.form["MinPrice"]:
                        minPrice = request.form["MinPrice"]
                    MaxPrice = 10000000000000000
                    if request.form["MaxPrice"]:
                        MaxPrice = request.form["MaxPrice"]
                    MinTime = "00:00:00"
                    if request.form["MinTime"]:
                        MinTime = request.form["MinTime"]
                    MaxTime = "23:59:59"
                    if request.form["MaxTime"]:
                        MaxTime = request.form["MaxTime"]
                    From = "%"
                    if request.form["From"]:
                        From = request.form["From"]
                    To = "%"
                    if request.form["To"]:
                        To = request.form["To"]
                    FCName = "%"  
                    if request.form["Flightcode"]:
                        FCName = request.form["Flightcode"]
                    ACName = "%"
                    if request.form["Aircraft"]:
                        ACName = request.form["Aircraft"]

                    query = ("""SELECT FCID, FCName, ACName, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport 
                                FROM    
                                    (SELECT FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport
                                    FROM ((SELECT FCID as FCIDold, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, Portname as DepartureAirport
                                    FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
                                    WHERE Portname LIKE %s) as Departure
                                    INNER JOIN 
                                    (SELECT Portname as ArrivalAirport, FCID
                                    FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
                                    WHERE Portname LIKE %s) as Arrival 
                                    ON Departure.FCIDold = Arrival.FCID)) as flightcode 
                                INNER JOIN aircraft ON flightcode.ACID LIKE aircraft.ACID 
                                WHERE Price_E >= %s AND Price_E <= %s AND ScheduledDepartureTime >= %s AND ScheduledDepartureTime <= %s  AND ACName LIKE %s AND FCName LIKE %s""")
                    data = (From, To, minPrice, MaxPrice, MinTime,
                            MaxTime, ACName, FCName)

                    cnx = _connector.connect(
                        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                    cursor = cnx.cursor()

                    cursor.execute(query, data)

                    flightcodes = cursor.fetchall()

                    cursor.close()
                    cnx.close()

                    return render_template('emp_flightcode.html', flightcodeList = flightcodes, SearchOptionsFROM = SearchOptionsFROM, SearchOptionsTO = SearchOptionsTO, SearchOptionsFlightcode = SearchOptionsFlightcode, SearchOptionsAircraft = SearchOptionsAircraft)

                else:


                    flightCode = request.form
                    FCName = flightCode['FCName']
                    ACName = flightCode['ACName']
                    Price_E = flightCode['Price_E']
                    Price_B = flightCode['Price_B']
                    Price_F = flightCode['Price_F']
                    Miles_E = flightCode['Miles_E']
                    Miles_B = flightCode['Miles_B']
                    Miles_F = flightCode['Miles_F']
                    ScheduledDepartureTime = flightCode['ScheduledDepartureTime']
                    DayWeek = flightCode['DayWeek']
                    FlightDuration = flightCode['FlightDuration']
                    DepartureAirport = flightCode['DepartureAirport']
                    ArrivalAirport = flightCode['ArrivalAirport']

                    query_update = ("REPLACE INTO flightcode(FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport ) VALUES ( %s, (SELECT ACID FROM aircraft WHERE aircraft.ACName = %s), %s, %s, %s, %s, %s, %s, %s, %s, %s, (SELECT APID FROM airport WHERE airport.PortName = %s), (SELECT APID FROM airport WHERE airport.PortName = %s)) ")
                    data_update = (FCName,ACName, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F,
                                ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport)
                    
                    print(data_update)

                    cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                                database='flightproject')
                    cursor = cnx.cursor()
                    try:
                        cursor.execute(query_update, data_update)
                    except Exception:
                            flash("Something went wrong")
                            return redirect(url_for("flightcodes"))
                    cnx.commit()
                    cursor.close()
                    cnx.close()

                    flash("The flightcode has been updated/inserted!", "info")

                    return redirect(url_for('flightcodes'))
            else:
                query = ("""SELECT FCID, FCName, ACName, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport 
                            FROM
                                (SELECT FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport
                                FROM ((SELECT FCID as FCIDold, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, Portname as DepartureAirport
                                FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
                                WHERE Portname LIKE "%") as Departure
                                INNER JOIN 
                                (SELECT Portname as ArrivalAirport, FCID
                                FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
                                WHERE Portname LIKE "%") as Arrival 
                                ON Departure.FCIDold = Arrival.FCID)) as flightcode 
                            INNER JOIN aircraft ON flightcode.ACID LIKE aircraft.ACID""")

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query)

                flightcodes = cursor.fetchall()

                cursor.close()
                cnx.close()

                return render_template('emp_flightcode.html', flightcodeList=flightcodes, SearchOptionsFROM = SearchOptionsFROM, SearchOptionsTO = SearchOptionsTO, SearchOptionsFlightcode = SearchOptionsFlightcode, SearchOptionsAircraft = SearchOptionsAircraft)
        else:
            return render_template('home.html')
    else:
        return redirect(url_for("login"))


@app.route('/flights', methods=['GET', 'POST'])
def flights():
    if "user" in session:
        if session["emp"] == "off":

            query = ('SELECT DISTINCT PortName FROM flightcode INNER JOIN Airport ON flightcode.DepartureAirport = airport.APID')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsFROM = cursor.fetchall()

            cursor.close()
            cnx.close()

            query = ('SELECT DISTINCT PortName FROM flightcode INNER JOIN Airport ON flightcode.ArrivalAirport = airport.APID')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsTO = cursor.fetchall()

            cursor.close()
            cnx.close()

            if request.method == 'POST':
                if request.form["Search"] == "Search":

                    minPrice = 0
                    if request.form["MinPrice"]:
                        minPrice = request.form["MinPrice"]
                    MaxPrice = 10000000000000000
                    if request.form["MaxPrice"]:
                        MaxPrice = request.form["MaxPrice"]
                    MinTime = "00:00:00"
                    if request.form["MinTime"]:
                        MinTime = request.form["MinTime"]
                    MaxTime = "23:59:59"
                    if request.form["MaxTime"]:
                        MaxTime = request.form["MaxTime"]
                    From = "%"
                    if request.form["From"]:
                        From = request.form["From"]
                    To = "%"
                    if request.form["To"]:
                        To = request.form["To"]

                    query = ("""SELECT * FROM 
                                    (SELECT FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport
                                    FROM ((SELECT FCID as FCIDold, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, Portname as DepartureAirport
                                    FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
                                    WHERE Portname LIKE %s) as Departure
                                    INNER JOIN 
                                    (SELECT Portname as ArrivalAirport, FCID
                                    FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
                                    WHERE Portname LIKE %s) as Arrival 
                                    ON Departure.FCIDold = Arrival.FCID)) as flightcode
                                WHERE Price_E >= %s AND Price_E <= %s AND ScheduledDepartureTime >= %s AND ScheduledDepartureTime <= %s """)
                    data = (From, To, minPrice, MaxPrice, MinTime,
                            MaxTime,)

                    cnx = _connector.connect(
                        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                    cursor = cnx.cursor()

                    cursor.execute(query, data)

                    flightcodes = cursor.fetchall()

                    cursor.close()
                    cnx.close()


                    return render_template('flights.html', flightcodeList = flightcodes, SearchOptionsFROM = SearchOptionsFROM, SearchOptionsTO = SearchOptionsTO)
                return render_template('flights.html')
            else:
                query = ("""SELECT * FROM (SELECT FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport
                                    FROM ((SELECT FCID as FCIDold, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, Portname as DepartureAirport
                                    FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
                                    WHERE Portname LIKE "%") as Departure
                                    INNER JOIN 
                                    (SELECT Portname as ArrivalAirport, FCID
                                    FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
                                    WHERE Portname LIKE "%") as Arrival 
                                    ON Departure.FCIDold = Arrival.FCID)) as flightcode""")

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query)

                flightcodes = cursor.fetchall()

                cursor.close()
                cnx.close()

                return render_template('flights.html', flightcodeList = flightcodes, SearchOptionsFROM = SearchOptionsFROM, SearchOptionsTO = SearchOptionsTO)
        else:
            return render_template('home.html')
    else:
        return redirect(url_for("login"))


@app.route('/ticketsupport=<TID>', methods=['GET', 'POST'])
def supportDisplay(TID):
    if "user" in session:
        if session["emp"] == "on":
            if request.method == "POST":

                StatusDisplay = request.form["status"]

                ## Update request, Update reply and status ##            
                if request.form["update"] == "on":
                    query_update = (
                        "UPDATE ticketsupport SET Status = %s, Reply = %s WHERE UID = %s AND FCID = %s AND DepartureTime = %s AND TID = %s")
                    data_update = ("F", request.form["reply"], request.form["UID"],
                                   request.form["FCID"], request.form["DepartureTime"], request.form["TID"],)

                    cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                                  database='flightproject')

                    cursor = cnx.cursor()

                    cursor.execute(query_update, data_update)

                    cnx.commit()

                    cursor.close()
                    cnx.close()
                    flash("Reply has been send.")

                    return redirect(url_for("ticketsupport"))

                ## Dsiplay Content and/or Reply ##

                query = (
                    'SELECT content,reply FROM ticketsupport WHERE UID = %s AND FCID = %s AND DepartureTime = %s AND TID = %s')

                data = (request.form["UID"], request.form["FCID"],
                        request.form["DepartureTime"], TID,)

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query, data)

                content = cursor.fetchall()

                cursor.close()
                cnx.close()

                return render_template('emp_supportDisplay.html', content = content, data = data, StatusDisplay = StatusDisplay)
            else:
                return redirect(url_for("ticketsupport"))
        else:
            if request.method == "POST":

                ## Dsiplay Content and/or Reply ##

                query = (
                    'SELECT content,reply FROM ticketsupport WHERE UID = %s AND FCID = %s AND DepartureTime = %s AND TID = %s')

                data = (session["user"], request.form["FCID"],
                        request.form["DepartureTime"], TID,)
                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query, data)

                content = cursor.fetchall()

                cursor.close()
                cnx.close()

                return render_template('supportDisplay.html', content=content)
            else:
                return redirect(url_for("ticketsupport"))

    else:
        return redirect(url_for("login"))


@app.route('/supportrequest', methods=['GET', 'POST'])
def supportrequest():
    if "user" in session:
        if session["emp"] == "off":
            if request.method == 'POST':
                if request.form["create"] == "on":
                    ## Get next TID ##
                    query = (
                        'SELECT COUNT(TID) FROM ticketsupport WHERE UID = %s AND FCID = %s AND DepartureTime = %s')

                    data = (session["user"], request.form["FCID"],
                            request.form["DepartureTime"],)
                    cnx = _connector.connect(
                        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                    cursor = cnx.cursor()

                    cursor.execute(query, data)

                    nextTID = cursor.fetchall()[0][0]

                    cursor.close()
                    cnx.close()

                    TID = nextTID + 1

                    ## Create new Support Ticket ##

                    Reply = ""
                    if request.form["cancel"] == "on":
                        Status = "PC"
                    else:
                        Status = "PR"

                    query_insert = (
                        "INSERT INTO ticketsupport(UID,FCID,DepartureTime,TID,Content,Reply,Status) VALUES (%s, %s, %s, %s, %s, %s, %s)")
                    data_insert = (session["user"], request.form["FCID"],
                                   request.form["DepartureTime"], TID, request.form["content"], Reply, Status)

                    cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                                  database='flightproject')

                    cursor = cnx.cursor()

                    cursor.execute(query_insert, data_insert)

                    cnx.commit()

                    cursor.close()
                    cnx.close()

                    flash("Request has been send.")
                    return redirect(url_for("ticketsupport"))

                else:

                    ## Check if a Ticket is still pending##
                    query = (
                        'SELECT TID FROM ticketsupport WHERE UID = %s AND FCID = %s AND DepartureTime = %s AND Status = %s')

                    data = (session["user"], request.form["FCID"],
                            request.form["DepartureTime"], "P",)
                    cnx = _connector.connect(
                        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                    cursor = cnx.cursor()

                    cursor.execute(query, data)

                    pending = cursor.fetchall()

                    cursor.close()
                    cnx.close()

                    if pending:
                        flash(
                            "Request failed, because there is still a pending request for this Ticket.")
                        return redirect(url_for("history"))

                    FCID = request.form["FCID"]
                    DepartureTime = request.form["DepartureTime"]
                    CancelRequest = request.form["cancel"]

                    return render_template('supportrequest.html', FCID=FCID, DepartureTime=DepartureTime, CancelRequest = CancelRequest)
            else:
                return redirect(url_for("home"))
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/ticketsupport', methods=['GET', 'POST'])
def ticketsupport():
    if "user" in session:
        if session["emp"] == "on":

            # Search for  all Support Tickets that are pending

            query = ("""SELECT DepartureAirport, ArrivalAirport, ticket.DepartureTime, Price, ticketsupport.Status, TID,ticket.FCID,ticket.UID 
                        FROM ticket  JOIN ticketsupport  
                        INNER JOIN (SELECT FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport
                                    FROM ((SELECT FCID as FCIDold, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, Portname as DepartureAirport
                                    FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
                                    WHERE Portname LIKE "%") as Departure
                                    INNER JOIN 
                                    (SELECT Portname as ArrivalAirport, FCID
                                    FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
                                    WHERE Portname LIKE "%") as Arrival 
                                    ON Departure.FCIDold = Arrival.FCID)) as flightcode
                        ON ticket.FCID = flightcode.FCID WHERE ticketsupport.Status LIKE %s AND ticket.FCID = ticketsupport.FCID AND ticket.UID = ticketsupport.UID AND ticket.DepartureTime = ticketsupport.DepartureTime""")

            data = ("P_",)
            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query, data)

            supportList = cursor.fetchall()

            cursor.close()
            cnx.close()

            return render_template('emp_ticketsupport.html', supportList=supportList)
        else:

            query = ('SELECT DISTINCT PortName FROM flightcode INNER JOIN Airport ON flightcode.DepartureAirport = airport.APID')


            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsFROM = cursor.fetchall()

            cursor.close()
            cnx.close()

            query = ('SELECT DISTINCT PortName FROM flightcode INNER JOIN Airport ON flightcode.ArrivalAirport = airport.APID')


            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsTO = cursor.fetchall()

            cursor.close()
            cnx.close()

            if request.method == "POST":
                if request.form["Search"] == "Search":

                    MinPrice = 0
                    if request.form["MinPrice"]:
                        MinPrice = request.form["MinPrice"]
                    MaxPrice = 10000000000000000
                    if request.form["MaxPrice"]:
                        MaxPrice = request.form["MaxPrice"]
                    MinDate = "1900-01-01 00:00:00"
                    if request.form["MinDate"]:
                        MinDate = request.form["MinDate"]
                    MaxDate = "3900-01-01 23:59:59"
                    if request.form["MaxDate"]:
                        MaxDate = request.form["MaxDate"]
                    From = "%"
                    if request.form["From"]:
                        From = request.form["From"]
                    To = "%"
                    if request.form["To"]:
                        To = request.form["To"]
                    Status = "%"
                    if request.form["status"] != "all":
                        Status = request.form["status"]

                    query = ("""SELECT DepartureAirport, ArrivalAirport, ticket.DepartureTime, Price, ticketsupport.Status, TID,ticket.FCID 
                                FROM ticket  JOIN ticketsupport  INNER JOIN 
                                                (SELECT FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport
                                                FROM ((SELECT FCID as FCIDold, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, Portname as DepartureAirport
                                                FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
                                                WHERE Portname LIKE %s ) as Departure
                                                INNER JOIN 
                                                (SELECT Portname as ArrivalAirport, FCID
                                                FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
                                                WHERE Portname LIKE %s) as Arrival 
                                                ON Departure.FCIDold = Arrival.FCID)) as flightcode 
                                ON ticket.FCID = flightcode.FCID 
                                WHERE ticket.UID = %s AND ticket.FCID = ticketsupport.FCID AND ticket.UID = ticketsupport.UID AND ticket.DepartureTime = ticketsupport.DepartureTime AND ticket.Price >= %s AND ticket.Price <= %s AND ticket.DepartureTime >= %s AND ticket.DepartureTime <= %s AND ticketsupport.status LIKE %s""")
                    data = (From, To, session["user"], MinPrice, MaxPrice, MinDate,
                            MaxDate, Status,)

                    cnx = _connector.connect(
                        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                    cursor = cnx.cursor()

                    cursor.execute(query, data)

                    tickets = cursor.fetchall()

                    cursor.close()
                    cnx.close()

                    return render_template('ticketsupport.html', supportList=tickets, SearchOptionsFROM = SearchOptionsFROM, SearchOptionsTO = SearchOptionsTO)
            else:

                # Search for Support Tickets

                query = ("""SELECT DepartureAirport, ArrivalAirport, ticket.DepartureTime, Price, ticketsupport.Status, TID,ticket.FCID 
                            FROM ticket  JOIN ticketsupport  INNER JOIN 
                                                (SELECT FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport
                                                FROM ((SELECT FCID as FCIDold, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, Portname as DepartureAirport
                                                FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
                                                WHERE Portname LIKE "%") as Departure
                                                INNER JOIN 
                                                (SELECT Portname as ArrivalAirport, FCID
                                                FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
                                                WHERE Portname LIKE "%") as Arrival 
                                                ON Departure.FCIDold = Arrival.FCID)) as flightcode   
                            ON ticket.FCID = flightcode.FCID WHERE ticket.UID = %s AND ticket.FCID = ticketsupport.FCID AND ticket.UID = ticketsupport.UID AND ticket.DepartureTime = ticketsupport.DepartureTime""")

                data = (session["user"],)
                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query, data)

                supportList = cursor.fetchall()

                cursor.close()
                cnx.close()

                return render_template('ticketsupport.html', supportList=supportList, SearchOptionsFROM = SearchOptionsFROM, SearchOptionsTO = SearchOptionsTO)
    else:
        return redirect(url_for("login"))


@app.route('/flight=<FCID>', methods=['GET', 'POST'])
def flightDisplay(FCID):
    if "user" in session:
        if request.method == 'POST':

            ## Check if User alrdy bought a ticket for this flight ##
            UID = session["user"]
            FCID = request.form["FCID"]
            DepartureTime = request.form["DepartureTime"]

            query = (
                'SELECT UID FROM ticket WHERE FCID = %s AND DepartureTime = %s AND UID = %s')
            data = (FCID, DepartureTime, UID,)
            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query, data)

            ticket = cursor.fetchone()

            cursor.close()
            cnx.close()

            if ticket:
                flash(
                    "You already have booked/reserved a Ticket for this Flight. Go to our History page for more info!")
                return redirect(url_for("flightDisplay", FCID=FCID))

            ## SeatUpgrade ##
            SeatType = request.form["type"]
            if request.form["SeatUpgrade"] == "on":
                if SeatType == "E":
                    SeatType = "B"
                else:
                    SeatType = "F"

            ## Check if Seat is still available ##
            if SeatType == "E":
                query = (
                    'SELECT FreeSeat_E FROM flight WHERE FCID = %s AND DepartureTime = %s')
                data = (FCID, DepartureTime,)
                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query, data)

                FreeSeats = cursor.fetchone()[0]

                cursor.close()
                cnx.close()

                if FreeSeats <= 0:
                    flash("The Seat you tried to book is not available anymore")
                    return redirect(url_for("flightDisplay", FCID=FCID))

            if SeatType == "B":
                query = (
                    'SELECT FreeSeat_B FROM flight WHERE FCID = %s AND DepartureTime = %s')
                data = (FCID, DepartureTime,)
                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query, data)

                FreeSeats = cursor.fetchone()[0]

                cursor.close()
                cnx.close()

                if FreeSeats <= 0:
                    flash("The Seat you tried to book is not available anymore")
                    return redirect(url_for("flightDisplay", FCID=FCID))

            if SeatType == "F":
                query = (
                    'SELECT FreeSeat_F FROM flight WHERE FCID = %s AND DepartureTime = %s')
                data = (FCID, DepartureTime,)
                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query, data)

                FreeSeats = cursor.fetchone()[0]

                cursor.close()
                cnx.close()

                if FreeSeats <= 0:
                    flash("The Seat you tried to book is not available anymore")
                    return redirect(url_for("flightDisplay", FCID=FCID))

            ## Generate Seat Number ##

            if SeatType == "E":
                query = (
                    'SELECT Seats_E FROM flightcode INNER JOIN aircraft ON flightcode.ACID = aircraft.ACID WHERE FCID = %s ')
            elif SeatType == "B":
                query = (
                    'SELECT Seats_B FROM flightcode INNER JOIN aircraft ON flightcode.ACID = aircraft.ACID WHERE FCID = %s ')
            else:
                query = (
                    'SELECT Seats_F FROM flightcode INNER JOIN aircraft ON flightcode.ACID = aircraft.ACID WHERE FCID = %s ')
            data = (FCID,)
            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query, data)

            MaxFreeSeats = cursor.fetchone()[0]

            cursor.close()
            cnx.close()

            Seat = MaxFreeSeats - FreeSeats + 1

            ## Add Extra Luggage and Costs ##
            if request.form["ExtraLuggage"] == "5":
                Luggage = float(request.form["Luggage"]) + 5
                Price = float(request.form["Price"]) + 20
            elif request.form["ExtraLuggage"] == "10":
                Luggage = float(request.form["Luggage"]) + 10
                Price = float(request.form["Price"]) + 35
            else:
                Luggage = float(request.form["Luggage"])
                Price = float(request.form["Price"])

            ## Generate Status ##
            if request.form["isbuy"] == "1":
                Status = "B"
            else:
                Status = "R"

            ## Ticket Insert ##
            UID = session["user"]
            Miles = request.form["Miles"]
            
            #----------------------------------------------------------------Try einfügen


            query_insert = (
                "INSERT INTO ticket(UID,FCID,DepartureTime,Price,Miles,Seat,Luggage,Type,Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            data_insert = (UID, FCID, DepartureTime, Price,
                           Miles, Seat, Luggage, SeatType, Status)

            cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                          database='flightproject')

            cursor = cnx.cursor()

            cursor.execute(query_insert, data_insert)

            cnx.commit()

            cursor.close()
            cnx.close()

            

            ##Send Email##

            query_get_email = ("SELECT Email FROM User WHERE UID = %s")
            data_get_email = (UID,)

            cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                          database='flightproject')

            cursor = cnx.cursor()

            cursor.execute(query_get_email, data_get_email)

            email_Address = cursor.fetchone()[0]

            cursor.close()
            cnx.close()

            ## Get FCName ## 

            query = ("SELECT FCName FROM flightcode WHERE FCID = %s")
            data = (FCID,)

            cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                          database='flightproject')

            cursor = cnx.cursor()

            cursor.execute(query, data)

            FCName = cursor.fetchone()[0]

            cursor.close()
            cnx.close()

            #email_Address = "siegbertschnoesel9@gmail.com"
            _email.send_email(email_Address, UID, FCName, DepartureTime,
                       Miles, Seat, Luggage, SeatType, Price)

            flash("Ticket has been booked!")
            return redirect(url_for("history"))
        else:

            # ------------------------------ Get available Flights------------------------------------------

            query_E = (
                'SELECT CAST(DepartureTime AS char) FROM flight WHERE FCID = %s AND FreeSeat_E > 0 AND DepartureTime > NOW()')

            query_B = (
                'SELECT CAST(DepartureTime AS char) FROM flight WHERE FCID = %s AND FreeSeat_B > 0 AND DepartureTime > NOW()')

            query_F = (
                'SELECT CAST(DepartureTime AS char) FROM flight WHERE FCID = %s AND FreeSeat_F > 0 AND DepartureTime > NOW()')

            data = (FCID,)

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')

            cursor = cnx.cursor()
            cursor.execute(query_E, data)
            flights_economy = cursor.fetchall()
            cursor.close()

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')

            cursor = cnx.cursor()
            cursor.execute(query_B, data)
            flights_business = cursor.fetchall()
            cursor.close()

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')

            cursor = cnx.cursor()
            cursor.execute(query_F, data)
            flights_firstclass = cursor.fetchall()
            cursor.close()

            cnx.close()

            # ------------------------------ Get Prices for Flights------------------------------------------

            query_conditions = ("SELECT FLOOR(Price_E * PriceMult) as Price_E,FLOOR(Luggage_E * LuggageMult) as Luggage_E,FLOOR(Miles_E * MilesMult) as Miles_E, FLOOR(Price_B * PriceMult) as Price_B,FLOOR(Luggage_B * LuggageMult) as Luggage_B,FLOOR(Miles_B * MilesMult) as Miles_B, FLOOR(Price_F * PriceMult) as Price_F,FLOOR(Luggage_F * LuggageMult) as Luggage_F,FLOOR(Miles_F * MilesMult) as Miles_F FROM tier, flightcode INNER JOIN aircraft ON flightcode.ACID = aircraft.ACID WHERE flightcode.FCID = %s and tier.tier = %s")

            data_conditions = (FCID, session["tier"],)

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')

            cursor = cnx.cursor()
            cursor.execute(query_conditions, data_conditions)
            flights_conditions = cursor.fetchall()
            cursor.close()

            cnx.close()

            return render_template('flightDisplay.html', FCID=FCID, flights_economy=flights_economy, flights_business=flights_business, flights_firstclass=flights_firstclass, flightcode_details=flights_conditions[0])
    else:
        return redirect(url_for("login"))


@app.route('/ticketconfirmation', methods=['GET', 'POST'])
def ticketconfirmation():
    if "user" in session:
        if request.method == 'POST':

            FCID = request.form["FCID"]

            ## Check if Reservation is possible ##

            if request.form["isbuy"] == "0":
                query = ('SELECT ReservationTime FROM tier WHERE tier.tier = %s')

                data = (session["tier"],)
                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query, data)

                DaysAble = cursor.fetchone()

                cursor.close()
                cnx.close()

                flighttime = _time.datetime.strptime(
                    request.form["DepartureTime"], '%Y-%m-%d %H:%M:%S')

                DaysTime = int(DaysAble[0])

                ReservationTime = _time.timedelta(days=DaysTime)
                delta = flighttime - _time.datetime.now()
                if delta > ReservationTime:
                    flash(
                        "You cant reservate this flight, because you dont have the necessary Tier. For more information visit the Tier Page ")
                    return redirect(url_for("flightDisplay", FCID=FCID))

            ## Check for SeatUpgrade ##

            if request.form["SeatUpgrade"] == "1":
                SeatUpgrade = 1
            else:
                query = ('SELECT SeatUpgrade FROM tier WHERE tier.tier = %s')

                data = (session["tier"],)
                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query, data)

                SeatUpgrade = cursor.fetchone()[0]

                cursor.close()
                cnx.close()

            SeatType = request.form["type"]

            # Check if Seats are available for in higher class

            if SeatUpgrade == 1:
                if SeatType == "E":
                    query = (
                        'SELECT FreeSeat_B FROM flight WHERE FCID = %s AND DepartureTime = %s')
                    data = (FCID, request.form["DepartureTime"],)
                    cnx = _connector.connect(
                        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                    cursor = cnx.cursor()

                    cursor.execute(query, data)

                    FreeSeats = cursor.fetchone()[0]

                    cursor.close()
                    cnx.close()
                    if FreeSeats <= 0:
                        SeatUpgrade = 0

                if SeatType == "B":
                    query = (
                        'SELECT FreeSeat_F FROM flight WHERE FCID = %s AND DepartureTime = %s')
                    data = (FCID, request.form["DepartureTime"],)
                    cnx = _connector.connect(
                        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                    cursor = cnx.cursor()

                    cursor.execute(query, data)

                    FreeSeats = cursor.fetchone()[0]

                    cursor.close()
                    cnx.close()

                    if FreeSeats <= 0:
                        SeatUpgrade = 0

                if SeatType == "F":
                    SeatUpgrade = 0

            ## Get Flightdetails ##

            query = (
                """SELECT DepartureAirport, ArrivalAirport 
                FROM 
                    (SELECT FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport
                    FROM ((SELECT FCID as FCIDold, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, Portname as DepartureAirport
                    FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
                    WHERE Portname LIKE "%") as Departure
                    INNER JOIN 
                    (SELECT Portname as ArrivalAirport, FCID
                    FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
                    WHERE Portname LIKE "%") as Arrival 
                    ON Departure.FCIDold = Arrival.FCID)) as flightcode
                WHERE FCID = %s""")

            data = (FCID,)
            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query, data)

            X = cursor.fetchone()

            From = X[0]
            To = X[1]

            cursor.close()
            cnx.close()

            ## Fill content ##

            content = []

            content.append(FCID)
            content.append(From)
            content.append(To)
            content.append(request.form["Price"])
            content.append(request.form["Miles"])
            content.append(request.form["Luggage"])
            content.append(request.form["type"])
            content.append(request.form["DepartureTime"])
            content.append(request.form["isbuy"])
            content.append(SeatUpgrade)

            return render_template('ticketconfirmation.html', content=content)
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))

    if "user" in session:
        if request.method == 'POST':
            TicketDetails = request.form
            FCID = TicketDetails['FCID']
            return render_template('ticketconfirmation.html', content=TicketDetails)
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/')
def backhome():
    return redirect(url_for("login"))


@app.route('/login')
def login():
    if "user" in session:
        return redirect(url_for("home"))
    else:
        return render_template('login.html')


@app.route('/ticketupdate', methods=['GET', 'POST'])
def ticketupdate():
    if "user" in session:
        if request.method == 'POST':
            if request.form["update"] == "pay":
                query_update = (
                    "UPDATE ticket SET status = %s WHERE UID = %s AND FCID = %s AND DepartureTime = %s")
                data_update = (
                    "B", request.form["UID"], request.form["FCID"], request.form["DepartureTime"],)

                cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                              database='flightproject')

                cursor = cnx.cursor()

                cursor.execute(query_update, data_update)

                cnx.commit()

                cursor.close()
                cnx.close()
                flash("The ticket has been payed.")
                return redirect(url_for("history"))

            if request.form["update"] == "cancel":
                query_update = (
                    "UPDATE ticket SET status = %s WHERE UID = %s AND FCID = %s AND DepartureTime = %s")
                data_update = (
                    "D", request.form["UID"], request.form["FCID"], request.form["DepartureTime"],)

                cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                              database='flightproject')

                cursor = cnx.cursor()

                cursor.execute(query_update, data_update)

                cnx.commit()

                cursor.close()
                cnx.close()

                ## Update Support Ticket ##

                query_update = (
                    "UPDATE ticketsupport SET Status = %s, Reply = %s WHERE UID = %s AND FCID = %s AND DepartureTime = %s AND TID = %s")
                data_update = ("F", request.form["reply"], request.form["UID"],
                               request.form["FCID"], request.form["DepartureTime"], request.form["TID"],)

                cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                              database='flightproject')

                cursor = cnx.cursor()

                cursor.execute(query_update, data_update)

                cnx.commit()

                cursor.close()
                cnx.close()

                flash("Flight has been cancelled.")
                return redirect(url_for("supportDisplay", TID=request.form["TID"]))

            if request.form["update"] == "reactivate":
                query_update = (
                    "UPDATE ticket SET status = %s WHERE UID = %s AND FCID = %s AND DepartureTime = %s")
                data_update = (
                    "B", request.form["UID"], request.form["FCID"], request.form["DepartureTime"],)

                cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                              database='flightproject')

                cursor = cnx.cursor()

                cursor.execute(query_update, data_update)

                cnx.commit()

                cursor.close()
                cnx.close()

                ## Update Support Ticket ##

                query_update = (
                    "UPDATE ticketsupport SET Status = %s, Reply = %s WHERE UID = %s AND FCID = %s AND DepartureTime = %s AND TID = %s")
                data_update = ("F", request.form["reply"], request.form["UID"],
                               request.form["FCID"], request.form["DepartureTime"], request.form["TID"],)

                cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                              database='flightproject')

                cursor = cnx.cursor()

                cursor.execute(query_update, data_update)

                cnx.commit()

                cursor.close()
                cnx.close()

                flash("Flight has been reactivated.")
                return redirect(url_for("supportDisplay", TID=request.form["TID"]))

            if request.form["update"] == "checkin":
                query_update = (
                    "UPDATE ticket SET status = %s WHERE UID = %s AND FCID = %s AND DepartureTime = %s")
                data_update = (
                    "C", request.form["UID"], request.form["FCID"], request.form["DepartureTime"],)

                cnx = _connector.connect(user='root', password='Fenrir03111995', host='localhost',
                                              database='flightproject')

                cursor = cnx.cursor()

                cursor.execute(query_update, data_update)

                cnx.commit()

                cursor.close()
                cnx.close()
                flash("You have successfully checked in.")
                return redirect(url_for("history"))

            flash("Something went wrong please contact an Employee")
            return redirect(url_for("history"))
        else:
            return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))


@app.route('/history', methods=['GET', 'POST'])
def history():
    if "user" in session:
        if session["emp"] == "off":

            query = ('SELECT DISTINCT PortName FROM flightcode INNER JOIN Airport ON flightcode.DepartureAirport = airport.APID')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsFROM = cursor.fetchall()

            cursor.close()
            cnx.close()

            query = ('SELECT DISTINCT PortName FROM flightcode INNER JOIN Airport ON flightcode.ArrivalAirport = airport.APID')

            cnx = _connector.connect(
                user='root', password='Fenrir03111995', host='localhost', database='flightproject')
            cursor = cnx.cursor()

            cursor.execute(query)

            SearchOptionsTO = cursor.fetchall()

            cursor.close()
            cnx.close()

            if request.method == 'POST':

                ## Search Bar Variables ##

                if request.form["Search"] == "Search":

                    minPrice = 0
                    if request.form["MinPrice"]:
                        minPrice = request.form["MinPrice"]
                    MaxPrice = 10000000000000000
                    if request.form["MaxPrice"]:
                        MaxPrice = request.form["MaxPrice"]
                    MinDate = "1900-01-01 00:00:00"
                    if request.form["MinDate"]:
                        MinDate = request.form["MinDate"]
                    MaxDate = "3900-01-01 23:59:59"
                    if request.form["MaxDate"]:
                        MaxDate = request.form["MaxDate"]
                    From = "%"
                    if request.form["From"]:
                        From = request.form["From"]
                    To = "%"
                    if request.form["To"]:
                        To = request.form["To"]
                    Status = "%"
                    if request.form["status"] != "all":
                        Status = request.form["status"]

                    query = ("""SELECT DepartureAirport, ArrivalAirport, DepartureTime, Price, Miles, Seat, Luggage, Type, Status, ticket.FCID, DATEDIFF( DepartureTime,NOW()) as CheckinTime 
                                FROM Ticket INNER JOIN (SELECT FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport
	                            FROM ((SELECT FCID as FCIDold, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, Portname as DepartureAirport
                                FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
                                WHERE Portname LIKE %s) as Departure
                                INNER JOIN 
                                (SELECT Portname as ArrivalAirport, FCID
                                FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
                                WHERE Portname LIKE %s) as Arrival 
                                ON Departure.FCIDold = Arrival.FCID)) as flightcode 
                                ON ticket.FCID = flightcode.FCID 
                                WHERE UID = %s AND Price >= %s AND Price <= %s AND DepartureTime >= %s AND DepartureTime <= %s  AND ticket.status LIKE %s""")
                    
                    data = (From, To, session["user"], minPrice, MaxPrice, MinDate,
                            MaxDate, Status,)

                    cnx = _connector.connect(
                        user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                    cursor = cnx.cursor()

                    cursor.execute(query, data)

                    flightcodes = cursor.fetchall()

                    cursor.close()
                    cnx.close()

                    return render_template('history.html', ticketList=flightcodes, UID=session["user"], SearchOptionsFROM = SearchOptionsFROM, SearchOptionsTO = SearchOptionsTO)

                return render_template('history.html')

            else:
                ## Get MilesThisYear ##
                query = ('SELECT MilesThisYear FROM user WHERE UID = %s')
                data = (session["user"],)

                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query, data)

                MilesThisYear = cursor.fetchone()[0]

                cursor.close()
                cnx.close()

                ## Search for all Tickets of the User ##

                query_tickets = ("""SELECT DepartureAirport, ArrivalAirport, DepartureTime, Price, Miles, Seat, Luggage, Type, Status, ticket.FCID, DATEDIFF( DepartureTime,NOW()) as CheckinTime 
                                    FROM Ticket 
                                    INNER JOIN (SELECT FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport
                                                FROM ((SELECT FCID as FCIDold, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, Portname as DepartureAirport
                                                FROM flightcode  INNER JOIN Airport ON DepartureAirport = APID
                                                WHERE Portname LIKE "%") as Departure
                                                INNER JOIN 
                                                (SELECT Portname as ArrivalAirport, FCID
                                                FROM flightcode  INNER JOIN Airport ON ArrivalAirport = APID
                                                WHERE Portname LIKE "%") as Arrival 
                                                ON Departure.FCIDold = Arrival.FCID)) as flightcode  
                                    ON ticket.FCID = flightcode.FCID WHERE UID = %s""")

                data_tickets = (session["user"],)
                cnx = _connector.connect(
                    user='root', password='Fenrir03111995', host='localhost', database='flightproject')
                cursor = cnx.cursor()

                cursor.execute(query_tickets, data_tickets)

                tickets = cursor.fetchall()

                cursor.close()
                cnx.close()

                return render_template('history.html', ticketList=tickets, MilesThisYear=MilesThisYear, UID=session["user"], SearchOptionsFROM = SearchOptionsFROM, SearchOptionsTO = SearchOptionsTO)
        else:
            return render_template('home.html')
    else:
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("pw", None)
    session.pop("emp", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
