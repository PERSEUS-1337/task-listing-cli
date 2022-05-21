from dotenv import load_dotenv
import mariadb
import os
import sys

load_dotenv()

try:
    connection = mariadb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database="task_listing",
    )

    cursor = connection.cursor()

except mariadb.Error as error:
    print(f"Error connecting to MariaDB Platform: {error}")
    sys.exit(1)
