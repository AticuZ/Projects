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

# Employee Username: 10 Password: a
INSERT INTO flightproject.User (UID, Password, FirstName, LastName, Birthday, Email, Tel, Address, IBAN, MilesThisYear, Tier, IsEmployee, Wage) VALUES("10", '$2b$12$x8II9JsBBT0qxWLqAUM8eOYXaFdTmPFH3gzxHNlk/pHlmUTbMDf.O', 'Siegbert', 'Schnösel', '2000-01-20', 'siegbertschnoesel9@gmail.com', "83956754654634", 'JStraße10Mainz', 'DE00000000000000000010', 0, 'G', 1, 1000000000);

