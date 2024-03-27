import sqlite3


class JobSearchDatabase:
    """Manages a database for storing company and messaging state information."""

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
          website TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messaging_state (
          id INTEGER PRIMARY KEY REFERENCES companies(id),
          message_state TEXT NOT NULL CHECK(message_state IN ('send_first_email', 'send_followup', 'none')),
          last_message_date DATE2
        )
        """)

        conn.commit()
        conn.close()

    def add_company(self, name, url):
        """Inserts a new company record into the database and creates an initial messaging state entry."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT COUNT(*) FROM companies WHERE name = ?
        """, (name,))

        count = cursor.fetchone()[0]
        if count > 0:
            return None

        cursor.execute("""
        INSERT INTO companies (name, website)
        VALUES (?, ?)""", (name, url))

        id = cursor.lastrowid  # Get the ID of the newly inserted company

        # Insert initial message state ('none')
        cursor.execute("""
        INSERT INTO messaging_state (id, message_state)
        VALUES (?, ?)""", (id, 'none'))

        conn.commit()
        conn.close()
        return id

    def get_company(self, id):
        """Retrieves a company record and its associated messaging state by ID."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT c.id, c.name, c.website, ms.message_state, ms.last_message_date
        FROM companies c
        INNER JOIN messaging_state ms ON c.id = ms.id
        WHERE c.id = ?""", (id,))  # Use a tuple for single value binding

        row = cursor.fetchone()

        if row:  # Check if a record was found
            company = {
                "id": row[0],
                "name": row[1],
                "website": row[2],
                "message_state": row[3],
                "last_message_date": row[4],
            }
            return company
        else:
            return None  # Return None if company not found

    def get_companies(self):
        """Retrieves all companies and their associated messaging state."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT c.id, c.name, c.website, ms.message_state, ms.last_message_date
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
            }
            companies.append(company)

        conn.close()
        return companies

    def update_message_state(self, id, new_message_state, last_message_date):
        valid_states = ("send_first_email", "send_followup", "none")
        if new_message_state not in valid_states: 
            raise('invalid message state: %s', new_message_state)
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE messaging_state
        SET message_state = ?, last_message_date = ?
        WHERE id = ?""", (new_message_state, last_message_date, id))

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
