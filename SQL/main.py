import sqlite3, os.path

def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "fiftyville.db")
    with sqlite3.connect(db_path) as db:
        cur = db.cursor()
        # GET REPORTS
        #reports = cur.execute("SELECT * FROM crime_scene_reports WHERE year = 2023 AND month = 7 AND day = 28 AND street = 'Humphrey Street'")
        #print(reports.fetchall())

        # GET INTERVEWS
        # interviews = cur.execute("SELECT transcript FROM interviews WHERE year = 2023 AND month = 7 AND day = 28")
        # for interview in interviews.fetchall():
        #     if "bakery" in interview[0]:
        #         print(interview)
        
        parking_query = """
            SELECT DISTINCT f.destination_airport_id, p.name, p.id
            FROM bakery_security_logs AS s
            JOIN people AS p ON s.license_plate = p.license_plate
            JOIN passengers AS pass ON p.passport_number = pass.passport_number
            JOIN flights AS f ON pass.flight_id = f.id
            WHERE s.year = 2023 AND s.month = 7 AND s.day = 28
            AND s.hour = 10 AND s.minute > 15 AND s.minute < 26
            AND s.activity = 'exit'
            AND f.year = 2023 AND f.month = 7 AND f.day = 29
            AND f.origin_airport_id = ?
            ORDER BY f.hour ASC, f.minute ASC
            LIMIT 1
        """

        airport = cur.execute("SELECT id FROM airports WHERE city = 'Fiftyville'")
        airport_id = airport.fetchone()[0]
        result = cur.execute(parking_query, (airport_id,)).fetchone()

        if result:
            destination_id = result[0]
            passenger_name = result[1]
            destination = cur.execute("SELECT full_name FROM airports WHERE id = ?", (destination_id,))
            destination_airport = destination.fetchone()[0]
            print("Destination Airport:", destination_airport)
            print("Thief name:", passenger_name)
        else:
            print("No matching flights found.")
       
        thief_cell = cur.execute("SELECT phone_number FROM people WHERE id = ?", (result[2],)).fetchall()[0]

        partner_cell = cur.execute("SELECT receiver FROM phone_calls WHERE duration < 60 AND caller = ?", thief_cell).fetchone()
        partner_name = cur.execute("SELECT name FROM people WHERE phone_number = ?", partner_cell).fetchall()[0]
        print("The thief's partner's name is:",partner_name[0])

if __name__ == "__main__":
    main()