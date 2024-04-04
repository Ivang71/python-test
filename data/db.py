import sqlite3


class JobSearchDatabase:
    def __init__(self, db_file="job_search.db"):
        self.db_name = db_file
        self.create_tables()


    def create_tables(self):
        """Creates tables for companies and messaging state if they don't exist."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          website TEXT,
          emails TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messaging_state (
          id INTEGER PRIMARY KEY REFERENCES companies(id),
          message_state TEXT NOT NULL CHECK(message_state IN ('send_first_email', 'send_followup', 'client_side_generation', 'none')),
          last_message_date DATE2
        )
        """)

        conn.commit()
        conn.close()


    def add_company(self, name, url, emails=[]):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(*) FROM companies WHERE name = ?
        """, (name,))

        count = cursor.fetchone()[0]
        if count > 0:
            return None

        # Convert email list to comma-separated string for storage
        email_string = ",".join(emails)

        cursor.execute("""
        INSERT INTO companies (name, website, emails)
        VALUES (?, ?, ?)""", (name, url, email_string))

        id = cursor.lastrowid  # Get the ID of the newly inserted company

        # Insert initial message state ('none')
        cursor.execute("""
        INSERT INTO messaging_state (id, message_state)
        VALUES (?, ?)""", (id, 'none'))

        conn.commit()
        conn.close()
        return id


    def get_company(self, id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT c.id, c.name, c.website, ms.message_state, ms.last_message_date, c.emails
        FROM companies c
        INNER JOIN messaging_state ms ON c.id = ms.id
        WHERE c.id = ?""", (id,))

        row = cursor.fetchone()

        if row:  # Check if a record was found
            company = {
                "id": row[0],
                "name": row[1],
                "website": row[2],
                "message_state": row[3],
                "last_message_date": row[4],
                "emails": row[5].split(",")  # Convert comma-separated string back to list
            }
            return company
        else:
            return None  # Return None if company not found


    def get_companies(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT c.id, c.name, c.website, ms.message_state, ms.last_message_date, c.emails
        FROM companies c
        INNER JOIN messaging_state ms ON c.id = ms.id
        """)

        rows = cursor.fetchall()
        companies = []
        for row in rows:
            company = {
                "id": row[0],
                "name": row[1],
                "website": row[2],
                "message_state": row[3],
                "last_message_date": row[4],
                "emails": row[5].split(",")  # Convert comma-separated string back to list
            }
            companies.append(company)

        conn.close()
        return companies
    
    
    def update_company(self, id, **kwargs):
        """example update_company(id, emails=["email1@example.com"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Check if the company exists
        cursor.execute("SELECT COUNT(*) FROM companies WHERE id = ?", (id,))
        count = cursor.fetchone()[0]
        if count == 0:
            raise ValueError("Company with ID {} does not exist".format(id))

        update_values = []
        values = []
        for field, value in kwargs.items():
            if field in ("name", "url"):
                update_values.append(f"{field} = ?")
                values.append(value)
            elif field == "emails":
                if not isinstance(value, list):
                    raise ValueError(f"Invalid value for 'emails': {value}. Must be a list.")
                # Convert email list to comma-separated string
                email_string = ",".join(value)
                update_values.append(f"emails = ?")
                values.append(email_string)
            else:
                raise ValueError(f"Invalid keyword argument: {field}")

        if update_values:
            sql = "UPDATE companies SET " + ",".join(update_values) + " WHERE id = ?"
            values.append(id)
            cursor.execute(sql, values)

        conn.commit()
        conn.close()


    def update_message_state(self, id, new_message_state):
        # for now, client_side_generation also marks unreacheable sites
        valid_states = ("send_first_email", "send_followup", "client_side_generation", "none")
        if new_message_state not in valid_states: 
            raise('invalid message state: %s', new_message_state)
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE messaging_state
        SET message_state = ?
        WHERE id = ?""", (new_message_state, id))

        conn.commit()
        conn.close()
        
    
    def does_company_exist(self, name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(*) FROM companies WHERE name = ?
        """, (name,))

        count = cursor.fetchone()[0]
        conn.close()
        return count > 0




if __name__ == "__main__":
    db = JobSearchDatabase()
