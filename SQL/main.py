import sqlite3, os.path

def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "fiftyville.db")
    with sqlite3.connect(db_path) as db:
        cur = db.cursor()

    bank_accounts = cur.execute("SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28 AND transaction_type = 'withdraw'").fetchall()

    ids = [] # IDS OF PEOPLE WHO WITHDREW ON THE DAY OF THE ROBBERY
    person_ids = cur.execute("SELECT account_number ,person_id FROM bank_accounts").fetchall()
    for item in person_ids:
        account_no  = item[0]
        person_id = item[1]
        for account in bank_accounts:
            if account[0] == account_no:
                ids.append(person_id)

    # GET PASSPORTS OF PEOPLE WHO LEFT BAKERY WITHIN 10 MINUTES AFTER ROBBERY
    passports = cur.execute("SELECT passport_number FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 26 AND activity = 'exit')").fetchall()
    passports = [passport[0] for passport in passports]
    
    #INFO OF PEOPLE WHO CALLED FOR LESS THAN 60s AND LEFT BAKER WITHIN 10 MINUTES
    people = []
    all_people = cur.execute("SELECT * FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60 )").fetchall()
    
    for person in all_people:
        if person[3] in passports:
            people.append(person)

    # INFOR OF PEOPLE WHO WITHDEW AND CALLED FOR LESS THAN 60s AND LEFT BAKER WITHIN 10 MINUTES
    people2 = []
    people2_passports = []

    for person in people:
        if person[0] in ids:
            people2.append(person)
            people2_passports.append(person[3])

    #FLIGHTS THAT HAPPENED THE NEXT DAY FROM FIFTYVILLE
    airport_id = cur.execute("SELECT id FROM airports WHERE city = 'Fiftyville'").fetchone()

    # GET FLIGHTS FOLLOWING DAY
    flights = cur.execute("SELECT id,destination_airport_id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 AND origin_airport_id = ? ORDER BY hour ASC, minute ASC", airport_id).fetchall()
    flight_ids = [flight[0] for flight in flights]

    placeholders = ', '.join(['?'] * len(people2_passports))
    query = f"SELECT flight_id FROM passengers WHERE passport_number IN ({placeholders})"
    passengers = cur.execute(query, tuple(people2_passports)).fetchall()
    passengers = [passenger[0] for passenger in passengers]
  
    # GET CORRECT FLIGHT ID
    correct_flight = 0
    for id in flight_ids:
        if id in passengers:
            correct_flight += id
            break

    # GET DESTINATION PLACE
    destination_id = 0
    for flight in flights:
        if correct_flight == flight[0]:
            destination_id += flight[1]
            break
    destination = cur.execute("SELECT city FROM airports WHERE id = ?", (destination_id,)).fetchone()

    # GET THIEF PASSPORT NUMBER
    query = f"SELECT passport_number FROM passengers WHERE flight_id = ? AND passport_number IN ({placeholders})"
    thief_passport = cur.execute(query,(correct_flight,) + tuple(people2_passports)).fetchone()

    # GET THIEF DETAILS
    thief = cur.execute("SELECT name, phone_number FROM people WHERE passport_number = ?",thief_passport).fetchone()

    # GET ACCOMPLICE PHONE NUMBER
    partner_num = cur.execute("SELECT receiver FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60 AND caller = ?", (thief[1],)).fetchone()

    # GET PARTNER Name
    partner = cur.execute("SELECT name FROM people WHERE phone_number = ?",partner_num).fetchone()

    print("The thief is :", thief[0])
    print("The accomplice is :", partner[0])
    print("City thief escaped to :", destination[0])
    
main()