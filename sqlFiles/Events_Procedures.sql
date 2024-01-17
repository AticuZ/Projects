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

DROP EVENT TierUpdate;
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