import psycopg2
def create_table(conn):
    try:
        csr =  conn.cursor()
        csr.execute(
        """
        CREATE TABLE IF NOT EXISTS message (
            id SERIAL PRIMARY KEY,
            message VARCHAR(100)
        )
        """
        )
        conn.commit()
        return  print("Create Table Success")
    except (Exception ,psycopg2.Error) as error:
        print(f"Error getting progress",error)
        return None