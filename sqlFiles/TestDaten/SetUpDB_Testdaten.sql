SET GLOBAL event_scheduler = ON;

USE flightproject;

DROP TABLE IF EXISTS OfferTo;
DROP TABLE IF EXISTS SpecialOffer;
DROP TABLE IF EXISTS TicketSupport;
DROP TABLE IF EXISTS Ticket;
DROP TABLE IF EXISTS Flight;
DROP TABLE IF EXISTS FlightCode;
DROP TABLE IF EXISTS Aircraft;
DROP TABLE IF EXISTS Airport;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Tier;


CREATE TABLE Tier(
	Tier					ENUM('B', 'S', 'G') PRIMARY KEY,
	PriceMult				FLOAT NOT NULL CHECK(PriceMult > 0), 
	LuggageMult				FLOAT NOT NULL CHECK(LuggageMult > 0),
	MilesMult				FLOAT NOT NULL CHECK(MilesMult > 0),
	SeatUpgrade				BOOLEAN NOT NULL, 
	ReservationTime			INTEGER NOT NULL
);

CREATE TABLE User(
	UID						VARCHAR(100) PRIMARY KEY,  
	Password				VARCHAR(100) NOT NULL,
	FirstName				VARCHAR(50) NOT NULL,
	LastName				VARCHAR(50) NOT NULL,
    Birthday				DATE NOT NULL,
	Email					VARCHAR(50) NOT NULL,
	Tel						VARCHAR(100) NOT NULL,
	Address					VARCHAR(50) NOT NULL,
	IBAN					VARCHAR(22) NOT NULL,
    MilesThisYear			INTEGER DEFAULT 0 CHECK(MilesThisYear >= 0),
    Tier					ENUM('B', 'S', 'G') DEFAULT 'B' REFERENCES Tier(Tier),
    IsEmployee				BOOLEAN DEFAULT 0,
    Wage					INTEGER DEFAULT 0 CHECK(Wage >= 0)
);

CREATE TABLE Airport(
	APID 					INTEGER PRIMARY KEY AUTO_INCREMENT,
    PortName				VARCHAR(50) NOT NULL
);

CREATE TABLE Aircraft(
	ACID					INTEGER PRIMARY KEY AUTO_INCREMENT,
    ACName					VARCHAR(50) UNIQUE NOT NULL,
	Seats_E					INTEGER NOT NULL CHECK(Seats_E > 0), 
	Seats_B					INTEGER NOT NULL CHECK(Seats_B > 0),
	Seats_F					INTEGER NOT NULL CHECK(Seats_F >= 0),
	Luggage_E				FLOAT NOT NULL CHECK(Luggage_E > 0), 
	Luggage_B				FLOAT NOT NULL CHECK(Luggage_B > 0),
	Luggage_F				FLOAT NOT NULL CHECK(Luggage_F >= 0),
    MaxLuggage				FLOAT NOT NULL CHECK(MaxLuggage > 0)
);

CREATE TABLE FlightCode(
	FCID					INTEGER PRIMARY KEY AUTO_INCREMENT,
    FCName					VARCHAR(20) UNIQUE NOT NULL,
    ACID					INTEGER REFERENCES Aircraft(ACID),
	Price_E					FLOAT NOT NULL CHECK(Price_E > 0),
	Price_B					FLOAT NOT NULL CHECK(Price_B > 0),
	Price_F					FLOAT,
	Miles_E					FLOAT NOT NULL CHECK(Miles_E > 0),
	Miles_B					FLOAT NOT NULL CHECK(Miles_B > 0),
	Miles_F					FLOAT,
	ScheduledDepartureTime	TIME NOT NULL,
	DayWeek					ENUM('0', '1', '2', '3', '4', '5', '6'),
	FlightDuration			INTEGER NOT NULL,
	DepartureAirport		INTEGER REFERENCES Airport(APID), 
	ArrivalAirport			INTEGER REFERENCES Airport(APID)
);

CREATE TABLE Flight(
	FCID					INTEGER REFERENCES FlightCode(FCID),
	DepartureTime			DATETIME,
	ArrivalTime				DATETIME NOT NULL,
	FreeSeat_E				INTEGER DEFAULT 0 CHECK(FreeSeat_E >= 0), 
	FreeSeat_B				INTEGER DEFAULT 0 CHECK(FreeSeat_B >= 0),
	FreeSeat_F				INTEGER DEFAULT 0 CHECK(FreeSeat_F >= 0),
	PRIMARY KEY (FCID,DepartureTime)
);

CREATE TABLE Ticket(
	UID						VARCHAR(50) REFERENCES Client(UID),
	FCID					INTEGER REFERENCES FlightCode(FCID),
	DepartureTime			DATETIME REFERENCES Flight(DepartureTime), 
    Price					INTEGER NOT NULL CHECK(Price > 0),
	Miles					INTEGER NOT NULL CHECK(Miles > 0),
	Seat					INTEGER NOT NULL CHECK(Seat > 0),
	Luggage					INTEGER NOT NULL CHECK(Luggage > 0),
	Type					ENUM('E', 'B', 'F') NOT NULL, 
	Status					ENUM('R', 'B', 'C', 'F', 'D') NOT NULL,  
	PRIMARY KEY (UID,FCID,DepartureTime)
);

CREATE TABLE TicketSupport(
	UID						VARCHAR(100) REFERENCES Client(UID),
	FCID					INTEGER REFERENCES FlightCode(FCID),
	DepartureTime			DATETIME REFERENCES Flight(DepartureTime), 
	TID						INTEGER,
	Content					TEXT NOT NULL,
	Reply					TEXT,
	Status					ENUM('PC','PR', 'F') DEFAULT 'PC',  
	PRIMARY KEY (UID,FCID,DepartureTime,TID)
);

CREATE TABLE SpecialOffer(
	FCID					INTEGER REFERENCES FlightCode(FCID),  
	OID						INTEGER AUTO_INCREMENT,
    OName					VARCHAR(20) NOT NULL,
	PriceMult				FLOAT DEFAULT 1 CHECK(PriceMult >= 0),
	LuggageMult				FLOAT DEFAULT 1 CHECK(LuggageMult >= 0),
	MilesMult				FLOAT DEFAULT 1 CHECK(MilesMult >= 0),
	SeatUpgrade				BOOLEAN DEFAULT 0,
	ReservationTime			INTEGER DEFAULT 0 CHECK(ReservationTime >= 0), 
	Status					BOOLEAN DEFAULT 0,
	PRIMARY KEY (OID,FCID),
    UNIQUE(FCID,OName)
);

CREATE TABLE OfferTo(
	FCID					INTEGER REFERENCES FlightCode(FCID),
	OID						INTEGER REFERENCES SpecialOffer(OID),
	UID						VARCHAR(100) REFERENCES Client(UID),
	PRIMARY KEY (FCID,OID,UID)
);



INSERT INTO flightproject.Flight(FCID, DepartureTime, ArrivalTime, FreeSeat_E, FreeSeat_B, FreeSeat_F) VALUES(4, '2020-10-01 08:00:00', '2020-10-01 09:30:00', 13, 5, 0);
INSERT INTO flightproject.Flight(FCID, DepartureTime, ArrivalTime, FreeSeat_E, FreeSeat_B, FreeSeat_F) VALUES(4, '2020-10-08 08:00:00', '2020-10-01 09:30:00', 32, 5, 2);
INSERT INTO flightproject.Flight(FCID, DepartureTime, ArrivalTime, FreeSeat_E, FreeSeat_B, FreeSeat_F) VALUES(3, '2020-10-28 20:00:00', '2020-10-28 21:00:00',40, 5, 3);
INSERT INTO flightproject.Flight(FCID, DepartureTime, ArrivalTime, FreeSeat_E, FreeSeat_B, FreeSeat_F) VALUES(37, '2020-10-15 16:00:00', '2020-10-15 17:00:00', 10, 5, 7);
INSERT INTO flightproject.Flight(FCID, DepartureTime, ArrivalTime, FreeSeat_E, FreeSeat_B, FreeSeat_F) VALUES(37, '2020-10-22 16:00:00', '2020-10-22 17:00:00', 5, 7, 13);
INSERT INTO flightproject.Flight(FCID, DepartureTime, ArrivalTime, FreeSeat_E, FreeSeat_B, FreeSeat_F) VALUES(37, '2020-10-29 16:00:00', '2020-10-22 17:00:00', 5, 7, 13);




INSERT INTO flightproject.Ticket(UID, FCID, DepartureTime, Price, Miles, Seat, Luggage, Type, Status) VALUES("BronzeClient", 4, '2020-10-01 08:00:00', 900, 35, 13, 15, 'E', 'F');
INSERT INTO flightproject.Ticket(UID, FCID, DepartureTime, Price, Miles, Seat, Luggage, Type, Status) VALUES("BronzeClient", 4, '2020-10-08 08:00:00', 900, 35, 13, 15, 'E', 'D');
INSERT INTO flightproject.Ticket(UID, FCID, DepartureTime, Price, Miles, Seat, Luggage, Type, Status) VALUES("BronzeClient", 3, '2020-10-28 20:00:00', 90, 8, 21, 15, 'E', 'B');
INSERT INTO flightproject.Ticket(UID, FCID, DepartureTime, Price, Miles, Seat, Luggage, Type, Status) VALUES("BronzeClient", 37, '2020-11-15 16:00:00', 950, 30, 6, 15, 'E', 'B');
INSERT INTO flightproject.Ticket(UID, FCID, DepartureTime, Price, Miles, Seat, Luggage, Type, Status) VALUES("BronzeClient", 37, '2020-11-22 16:00:00', 2000, 60, 3, 40, 'F', 'R');
INSERT INTO flightproject.Ticket(UID, FCID, DepartureTime, Price, Miles, Seat, Luggage, Type, Status) VALUES("BronzeClient", 37, '2020-11-29 16:00:00', 2000, 60, 3, 40, 'F', 'D');




DELIMITER $$
CREATE TRIGGER CorrectLuggageinFirstClassOrBusinessOnInser
BEFORE INSERT ON aircraft
FOR EACH ROW
BEGIN
	IF NEW.Luggage_F > ( NEW.MaxLuggage/(2*(NEW.Seats_E + NEW.Seats_B + NEW.Seats_F)) ) OR NEW.Luggage_B > ( NEW.MaxLuggage/(2*(NEW.Seats_E + NEW.Seats_B + NEW.Seats_F)) ) THEN
		SET NEW.ACName = NULL;
	END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER CorrectLuggageinFirstClassOrBusinessOnUPDATE
BEFORE UPDATE ON aircraft
FOR EACH ROW
BEGIN
	IF NEW.Luggage_F > ( NEW.MaxLuggage/(2*(NEW.Seats_E + NEW.Seats_B + NEW.Seats_F)) ) OR NEW.Luggage_B > ( NEW.MaxLuggage/(2*(NEW.Seats_E + NEW.Seats_B + NEW.Seats_F)) ) THEN
		SET NEW.ACName = NULL;
	END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER CorrectBirthdayInsert
BEFORE INSERT ON User
FOR EACH ROW
BEGIN
	IF NEW.Birthday > Current_Date() OR NEW.Birthday < DATE_ADD(Current_Date(), INTERVAL -125 YEAR) THEN
		SET NEW.UID = NULL;
	END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER CorrectBirthdayUpdate
BEFORE UPDATE ON User
FOR EACH ROW
BEGIN
	IF NEW.Birthday > Current_Date() OR NEW.Birthday < DATE_ADD(Current_Date(), INTERVAL -125 YEAR) THEN
		SET NEW.UID = NULL;
	END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER CorrectPriceAndMilesFirstClass
BEFORE INSERT ON FlightCode
FOR EACH ROW
BEGIN
	IF (NEW.Price_F IS NOT NULL AND NEW.Price_F < 0) OR (NEW.Miles_F IS NOT NULL AND NEW.Miles_F < 0) THEN
		SET NEW.FCID = NULL;
	END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER CorrectBaggageAmount
BEFORE INSERT ON Ticket
FOR EACH ROW
BEGIN
	IF 0 <> (SELECT Luggage_F FROM (Aircraft INNER JOIN FlightCode ON FlightCode.ACID = Aircraft.ACID) WHERE NEW.FCID = FCID) THEN
		IF NEW.Luggage > (2* (SELECT Luggage_F FROM (Aircraft INNER JOIN FlightCode ON FlightCode.ACID = Aircraft.ACID) WHERE NEW.FCID = FCID  )) THEN
			SET NEW.Luggage = (2*  (SELECT Luggage_F FROM (Aircraft INNER JOIN FlightCode ON FlightCode.ACID = Aircraft.ACID) WHERE NEW.FCID = FCID  ));
		END IF;
	ELSE 
		IF NEW.Luggage > (2* (SELECT Luggage_B FROM (Aircraft INNER JOIN FlightCode ON FlightCode.ACID = Aircraft.ACID) WHERE NEW.FCID = FCID  )) THEN
			SET NEW.Luggage = (2*  (SELECT Luggage_B FROM (Aircraft INNER JOIN FlightCode ON FlightCode.ACID = Aircraft.ACID) WHERE NEW.FCID = FCID  ));
		END IF;
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER CorrectTicketTime
BEFORE INSERT ON Ticket
FOR EACH ROW
BEGIN
	IF NEW.DepartureTime < Current_Date() THEN
		SET NEW.UID = NULL AND NEW.FCID = NULL AND NEW.DepartureTime = NULL;
	END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER CorrectLuggageForAircraftFirstClass 
BEFORE INSERT ON Aircraft
FOR EACH ROW
BEGIN
	IF NEW.Seats_F > 0 AND NEW.Luggage_F < NEW.Luggage_B THEN
		SET NEW.ACID = NULL;
	END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER CorrectFlightTime
BEFORE INSERT ON Flight
FOR EACH ROW
BEGIN
	IF NEW.DepartureTime < Current_Date() OR NEW.ArrivalTime < Current_Date() THEN
		SET NEW.FCID = NULL AND NEW.DepartureTime = NULL;
	END IF;
END $$
DELIMITER ;

DELIMITER $$ 
CREATE TRIGGER UpdateFreeSeatOnBuyAndReserve
BEFORE INSERT ON Ticket
FOR EACH ROW 
BEGIN 

IF NEW.Type = 'E' THEN
UPDATE flightproject.Flight FL
SET FL.FreeSeat_E = FL.FreeSeat_E - 1
WHERE FL.FCID = NEW.FCID AND FL.DepartureTime = NEW.DepartureTime;

ELSEIF NEW.Type = 'B' THEN
UPDATE flightproject.Flight FL
SET FL.FreeSeat_B = FL.FreeSeat_B - 1
WHERE FL.FCID = NEW.FCID AND FL.DepartureTime = NEW.DepartureTime;

ELSE 
UPDATE flightproject.Flight FL
SET FL.FreeSeat_F = FL.FreeSeat_F - 1
WHERE FL.FCID = NEW.FCID AND FL.DepartureTime = NEW.DepartureTime;
END IF;

END$$
DELIMITER ;

DELIMITER $$ 
CREATE TRIGGER UpdateFreeSeatOnCancel
AFTER UPDATE ON Ticket
FOR EACH ROW 
BEGIN 

IF NEW.Status <> OLD.Status AND NEW.Status = 'D' THEN
UPDATE flightproject.Flight FL
SET FreeSeat_E = FreeSeat_E + 1
WHERE NEW.Type = 'E' AND NEW.FCID = FL.FCID AND NEW.DepartureTime = FL.DepartureTime;

UPDATE flightproject.Flight FL
SET FreeSeat_B = FreeSeat_B + 1
WHERE NEW.Type = 'B' AND NEW.FCID = FL.FCID AND NEW.DepartureTime = FL.DepartureTime;

UPDATE flightproject.Flight FL
SET FreeSeat_F = FreeSeat_F + 1
WHERE NEW.Type = 'F' AND NEW.FCID = FL.FCID AND NEW.DepartureTime = FL.DepartureTime;

END IF;

END$$
DELIMITER ;

DELIMITER $$ 
CREATE TRIGGER UpdateFreeSeatOnReactivation
AFTER UPDATE ON Ticket
FOR EACH ROW 
BEGIN 

IF OLD.Status = 'D' AND NEW.Status = 'B' THEN
UPDATE Flight
SET FreeSeat_E = FreeSeat_E - 1
WHERE NEW.Type = 'E' AND NEW.FCID = Flight.FCID AND NEW.DepartureTime = Flight.DepartureTime;

UPDATE Flight
SET FreeSeat_B = FreeSeat_B - 1
WHERE NEW.Type = 'B' AND NEW.FCID = Flight.FCID AND NEW.DepartureTime = Flight.DepartureTime;

UPDATE Flight
SET FreeSeat_F = FreeSeat_F - 1
WHERE NEW.Type = 'F' AND NEW.FCID = Flight.FCID AND NEW.DepartureTime = Flight.DepartureTime;

END IF;

END$$
DELIMITER ;

INSERT INTO Airport(APID, PortName) VALUES(1, 'Berlin');
INSERT INTO Airport(APID, PortName) VALUES(2, 'London');
INSERT INTO Airport(APID, PortName) VALUES(3, 'Beppu');
INSERT INTO Airport(APID, PortName) VALUES(4, 'Amsterdam');
INSERT INTO Airport(APID, PortName) VALUES(5, 'Narita');
INSERT INTO Airport(APID, PortName) VALUES(6, 'Cairo');
INSERT INTO Airport(APID, PortName) VALUES(7, 'Sydney');
INSERT INTO Airport(APID, PortName) VALUES(8, 'Frankfurt');

INSERT INTO flightproject.Tier(Tier, PriceMult, LuggageMult, MilesMult, SeatUpgrade, ReservationTime)  VALUES('B', 1, 1, 1, 0, 0);
INSERT INTO flightproject.Tier(Tier, PriceMult, LuggageMult, MilesMult, SeatUpgrade, ReservationTime)  VALUES('S', 0.8, 1.2, 2, 0, 50);
INSERT INTO flightproject.Tier(Tier, PriceMult, LuggageMult, MilesMult, SeatUpgrade, ReservationTime)  VALUES('G', 0.5, 1.3, 3, 1, 365);

INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("BronzeClient", '$2b$12$pNbhrEXNesXsMYL06nvTduRruS1es.8FeUz9.Kmdq.zh1jpri84Ce', 'Hans', 'Schmidt', '2000-01-20', 'siegbertschnoesel9@gmail.com', "956754653124634", 'AStraße1Mainz', 'DE00000000000000000001', 0, 'B', 0, 0);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("GoldClient", '$2b$12$pNbhrEXNesXsMYL06nvTduRruS1es.8FeUz9.Kmdq.zh1jpri84Ce', 'Siegbert', 'Schnösel', '2000-01-20', 'siegbertschnoesel9@gmail.com', "956754653124634", 'AStraße1Mainz', 'DE00000000000000000001', 0, 'G', 0, 0);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("1", '$2b$12$pNbhrEXNesXsMYL06nvTduRruS1es.8FeUz9.Kmdq.zh1jpri84Ce', 'Hans', 'Schmidt', '2000-01-20', 'siegbertschnoesel9@gmail.com', "956754653124634", 'AStraße1Mainz', 'DE00000000000000000001', 500, 'B', 0, 0);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("2", '$2b$12$h9PCH6Zc5zCVmrETrrZYCOUA6iCc5o62h/5ZLB.myiw.528A7KNIW', 'Peter', 'Müller', '2000-01-20', 'siegbertschnoesel9@gmail.com', "956754653454634", 'BStraße2Mainz', 'DE00000000000000000002', 100, 'S', 0, 0);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("3", '$2b$12$g8Oi1CUYshnueb/RPx1udeCjZtTEJLYVBVy/4rjE3YnLVdQKiNkzO', 'Johannes', 'Sahne', '2000-01-20', 'siegbertschnoesel9@gmail.com', "95670954654634", 'CStraße3Mainz', 'DE00000000000000000003', 2333, 'G', 0, 0);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("4", '$2b$12$h1EyeqcHiGGez7hp150t9O2UhE/YwjvLd5ycSIcxcJSkP6NhedNyC', 'Maike',' Milch', '2000-01-20', 'siegbertschnoesel9@gmail.com', "956754123654634", 'DStraße4Mainz', 'DE00000000000000000004', 500, 'B', 0, 0);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("5", '$2b$12$CFcZUgZ2LOIZ1Yr/bOvO7.bIwJTUblvyTxVLlsr0A6NT/7.J5Xdy.', 'Günther', 'Käse', '2000-01-20', 'siegbertschnoesel9@gmail.com', "912356754654634", 'EStraße5Mainz', 'DE00000000000000000005', 500, 'S', 0, 0);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("6", '$2b$12$1g95E5obYApNjP6g4nyMKOgD0Xr.cIkeUTjCa.0WAyHWR2KJJuQ7a', 'Dieter', 'Wurst', '2000-01-20', 'siegbertschnoesel9@gmail.com', "12956754654634", 'FStraße6Mainz', 'DE00000000000000000006', 500, 'S', 0, 0);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("7", '$2b$12$WBLUNgnICdDayGVBIfTU/eDyTnXNG/5UQQVRsCGp7vqP4Sa2nGCm2', 'Angela', 'Pizza', '2000-01-20', 'siegbertschnoesel9@gmail.com', "523956754654634", 'GStraße7Mainz', 'DE00000000000000000007', 1000, 'G', 0, 0);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("8", '$2b$12$eOH1DI6mtsVHXq4hi5VmieC49DpILC3.hRdVXt/zzh6FpDZFwnFHC', 'Joachim', 'Banana', '2000-01-20', 'siegbertschnoesel9@gmail.com', "573956754654634", 'HStraße8Mainz', 'DE00000000000000000008', 1000000000, 'B', 0, 0);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("9", '$2b$12$XigbtqXl.SQwcJQYTxp4UeVVR71/XblMnOPJqcMNugjBHnqxXWPla', 'Thaddäus ', 'Tentakel', '2000-01-20', 'siegbertschnoesel9@gmail.com', "278956754654634", 'IStraße9Mainz', 'DE00000000000000000009', 0, 'B', 1, 12);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("10", '$2b$12$x8II9JsBBT0qxWLqAUM8eOYXaFdTmPFH3gzxHNlk/pHlmUTbMDf.O', 'Siegbert', 'Schnösel', '2000-01-20', 'siegbertschnoesel9@gmail.com', "83956754654634", 'JStraße10Mainz', 'DE00000000000000000010', 0, 'G', 1, 1000000000);
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("123", '$2b$12$1SjI9mM6xQavzoOK2H/xiejx/PhZbNZM8goyDIKI5QExkOdDBjvLS', 'oof', 'oof',  '2000-01-20', 'siegbertschnoesel9@gmail.com', "456956754654634", 'oofStraßeYikes', 'DE00000000000000000011', 0, 'G', 1, 1000000000);

INSERT INTO flightproject.Aircraft(ACID, ACName, Seats_E, Seats_B, Seats_F, Luggage_E, Luggage_B, Luggage_F, MaxLuggage) VALUES(1, 'LittleGuy1', 100, 10, 0, 15, 25, 0, 5500);
INSERT INTO flightproject.Aircraft(ACID, ACName, Seats_E, Seats_B, Seats_F, Luggage_E, Luggage_B, Luggage_F, MaxLuggage) VALUES(2, 'NormalDude1', 200, 20, 5, 20, 30, 40, 18000);
INSERT INTO flightproject.Aircraft(ACID, ACName, Seats_E, Seats_B, Seats_F, Luggage_E, Luggage_B, Luggage_F, MaxLuggage) VALUES(3, 'BigBoy1', 1000, 100, 50, 25, 35, 50, 115000);

INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(1, 'DA001', 1, 200, 500, 0, 20, 30, 0, '08:00:00', '0', 115, 1, 2);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(2, 'DA002', 2, 800, 1200, 1600, 30, 45, 60, '08:00:00', 1, 780, '1', 3);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(3, 'DA003', 1, 90, 200, 0, 8, 15, 0, '20:00:00', '2', 90, 1, 4);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(4, 'DA004', 2, 900, 1400, 2000, 35, 50, 65, '08:00:00', '3', 835, 1, 5);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(5, 'DA005', 1, 330, 600, 0, 25, 40, 0, '08:00:00', '4', 230, 1, 6);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(6, 'DA006', 3, 1100, 2100, 3300, 40, 60, 80, '08:00:00', '5', 1300, 1, 7);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(7, 'DA007', 1, 180, 350, 0, 10, 20, 0, '08:00:00', '6', 70, 1, 8);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(8, 'DA008', 1, 180, 450, 0, 20, 30, 0, '14:00:00', '2', 115, 1, 2);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(9, 'DA009', 2, 800, 1200, 1600, 30, 45, 60, '14:00:00', '3', 780, 1, 3);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(10, 'DA010', 1, 110, 240, 0, 8, 15, 0, '14:00:00', '4', 90, 1, 4);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(11, 'DA011', 2, 1000, 1550, 2200, 35, 50, 65, '14:00:00', '5', 835, 1, 5);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(12, 'DA012', 1, 350, 650, 0, 25, 40, 0, '14:00:00', '6', 230, 1, 6);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(13, 'DA013', 3, 1000, 1900, 3000, 40, 60, 80, '14:00:00', '0', 1300, 1, 7);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(14, 'DA014', 1, 150, 300, 0, 10, 20, 0, '14:00:00', '1', 70, 1, 8);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(15, 'DA015', 1, 220, 550, 0, 20, 30, 0, '20:00:00', '4', 115, 1, 2);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(16, 'DA016', 2, 880, 1300, 1750, 30, 45, 60, '20:00:00', '5', 780, 1, 3);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(17, 'DA017', 1, 120, 260, 0, 8, 15, 0, '20:00:00', '6', 90, 1, 4);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(18, 'DA018', 2, 900, 1400, 2000, 35, 50, 65, '20:00:00', '0', 835, 1, 5);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(19, 'DA019', 1, 300, 550, 0, 25, 40, 0, '20:00:00', '1', 230, 1, 6);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(20, 'DA020', 3, 900, 1700, 2700, 40, 60, 80, '20:00:00', '2', 1300, 1, 7);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(21, 'DA021', 1, 150, 300, 0, 10, 20, 0, '20:00:00', '3', 70, 1, 8);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(22, 'DA022', 1, 200, 500, 0, 20, 30, 0, '10:00:00', '1', 115, 2, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(23, 'DA023', 2, 700, 1050, 1400, 30, 45, 60, '10:00:00', '2', 780, 3, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(24, 'DA024', 1, 100, 220, 0, 8, 15, 0, '10:00:00', '3', 90, 4, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(25, 'DA025', 2, 1000, 1550, 2200, 35, 50, 65, '10:00:00', '4', 835, 5, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(26, 'DA026', 1, 330, 600, 0, 25, 40, 0, '10:00:00', '5', 230, 6, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(27, 'DA027', 3, 1200, 2300, 3600, 40, 60, 80, '10:00:00', '6', 1300, 7, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(28, 'DA028', 1, 150, 300, 0, 10, 20, 0, '10:00:00', '0', 70, 8, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(29, 'DA029', 1, 200, 500, 0, 20, 30, 0, '15:00:00', '3', 115, 2, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(30, 'DA030', 2, 880, 1350, 1800, 30, 45, 60, '15:00:00', '4', 780, 3, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(31, 'DA031', 1, 110, 240, 0, 8, 15, 0, '15:00:00', '5', 90, 4, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(32, 'DA032', 2, 1050, 1750, 2400, 35, 50, 65, '15:00:00', '6', 835, 5, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(33, 'DA033', 1, 300, 550, 0, 25, 40, 0, '15:00:00', '0', 230, 6, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(34, 'DA034', 3, 1000, 1900, 3000, 40, 60, 80, '15:00:00', '1', 1300, 7, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(35, 'DA035', 1, 135, 270, 0, 10, 20, 0, '15:00:00', '2', 70, 8, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(36, 'DA036', 1, 220, 550, 0, 20, 30, 0, '16:00:00', '5', 115, 2, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(37, 'DA037', 2, 950, 1500, 2000, 30, 45, 60, '16:00:00', '6', 780, 3, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(38, 'DA038', 1, 100, 220, 0, 8, 15, 0, '16:00:00', '0', 90, 4, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(39, 'DA039', 2, 900, 1400, 2000, 35, 50, 65, '16:00:00', '1', 835, 5, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(40, 'DA040', 1, 270, 500, 0, 25, 40, 0, '16:00:00', '2', 230, 6, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(41, 'DA041', 3, 1000, 1900, 3000, 40, 60, 80, '16:00:00', '3', 1300, 7, 1);
INSERT INTO flightproject.FlightCode(FCID, FCName, ACID, Price_E, Price_B, Price_F, Miles_E, Miles_B, Miles_F, ScheduledDepartureTime, DayWeek, FlightDuration, DepartureAirport, ArrivalAirport) VALUES(42, 'DA042', 1, 165, 330, 0, 10, 20, 0, '16:00:00', '4', 70, 8, 1);


INSERT INTO flightproject.SpecialOffer(FCID, OID, OName, PriceMult, LuggageMult, MilesMult, SeatUpgrade, ReservationTime, Status) VALUES(6, 1,"Christmas Special", 0.1, 1, 5, 1, 0, 1);

INSERT INTO flightproject.OfferTo(FCID, OID, UID) VALUES(6, 1, "BronzeClient");



DROP PROCEDURE IF EXISTS TierUpdateManually;
DELIMITER $$
CREATE PROCEDURE TierUpdateManually()

BEGIN
	IF flightproject.User.MilesThisYear <= 100 THEN
		UPDATE flightproject.User 
		SET Tier = 'B';
	ELSEIF flightproject.User.MilesThisYear <= 1000 THEN
		UPDATE flightproject.User 
		SET Tier = 'S';    
	ELSE 
		UPDATE flightproject.User 
		SET Tier = 'G';
	END IF;

    UPDATE flightproject.User
    SET MilesThisYear = MilesThisYear * 0;
END $$

DELIMITER ;

DROP EVENT IF EXISTS TierUpdate;
DELIMITER $$
CREATE EVENT TierUpdate
ON SCHEDULE EVERY 1 YEAR
STARTS '2020-01-01 00:00:00'
DO

BEGIN
	CALL TierUpdateManually;
END $$

DELIMITER ;




DROP PROCEDURE IF EXISTS FlightAndMilesUpdateManually;
DELIMITER $$
CREATE PROCEDURE FlightAndMilesUpdateManually()
BEGIN
	UPDATE User, Ticket
	SET User.MilesThisYear = User.MilesThisYear + Ticket.Miles, Ticket.status = 'F'
	WHERE Ticket.Status <> 'R' AND Ticket.Status <> 'F' AND Ticket.Status <> 'D' AND Ticket.UID = User.UID AND Ticket.DepartureTime < CURRENT_TIMESTAMP;	
END $$

DELIMITER ;


DROP EVENT IF EXISTS FlightAndMilesUpdate;

DELIMITER $$
CREATE EVENT FlightAndMilesUpdate
ON SCHEDULE EVERY 1 DAY
STARTS '2020-01-01 00:00:00'
DO

BEGIN
	CALL FlightAndMilesUpdateManually; 
END $$

DELIMITER ;

DROP PROCEDURE IF EXISTS FreeReservedSeatsManually;
DELIMITER $$
CREATE PROCEDURE FreeReservedSeatsManually()
BEGIN
	UPDATE Ticket
	SET Ticket.status = 'D'
	WHERE Ticket.Status = 'R' AND Ticket.DepartureTime < DATE_ADD(CURRENT_TIMESTAMP, INTERVAL -4 DAY);		
END $$

DELIMITER ;

DROP EVENT IF EXISTS FreeReservedSeats;

DELIMITER $$
CREATE EVENT FreeReservedSeats
ON SCHEDULE EVERY 1 DAY
STARTS '2020-01-01 00:00:00'
DO

BEGIN
	CALL FreeReservedSeatsManually;
END $$

DELIMITER ;

DROP PROCEDURE IF EXISTS MakeFlightsManually;

DELIMITER $$
CREATE PROCEDURE MakeFlightsManually()
BEGIN
	 DECLARE x INT DEFAULT 0;
     WHILE x < 25 DO
		INSERT INTO Flight
		SELECT FCID, TIMESTAMP(DATE_ADD('2020-11-02', INTERVAL 7*x + CAST(DayWeek AS SIGNED) DAY), ScheduledDepartureTime), DATE_ADD(TIMESTAMP(DATE_ADD('2020-11-02', INTERVAL 7*x + CAST(DayWeek AS SIGNED) DAY), ScheduledDepartureTime), INTERVAL FlightDuration MINUTE), Seats_E, Seats_B, Seats_F
		FROM FlightCode
		INNER JOIN Aircraft ON FlightCode.ACID = Aircraft.ACID;
		#ORDER BY RAND()
		#LIMIT 20;
        SET x = x + 1;
	END WHILE;
END $$
DELIMITER ;

CALL MakeFlightsManually();

DROP EVENT IF EXISTS MakeFlights;

DELIMITER $$
CREATE EVENT MakeFlights
ON SCHEDULE EVERY 1 WEEK
STARTS '2020-11-02 00:00:00'
DO

BEGIN

INSERT INTO Flight
SELECT FCID, TIMESTAMP(DATE_ADD(CURRENT_DATE(), INTERVAL 25*7 + CAST(DayWeek AS SIGNED) DAY), ScheduledDepartureTime), TIMESTAMP(DATE_ADD(CURRENT_DATE(), INTERVAL 25*7 + CAST(DayWeek AS SIGNED) DAY), ScheduledArrivalTime), Seats_E, Seats_B, Seats_F
FROM FlightCode
INNER JOIN Aircraft ON FlightCode.ACID = Aircraft.ACID;
#ORDER BY RAND()
#LIMIT 20;

END $$

DELIMITER ;