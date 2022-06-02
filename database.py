from dotenv import load_dotenv
import mariadb
import os
import sys

load_dotenv()

# userInput = input("Enter user: ")
# userPW = input("Enter password: ")
# userHost = socket.gethostname()
# userPort = 3306

try:
    connection = mariadb.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database="task_listing",
    )
    # connection = mariadb.connect(
    #     user=userInput,
    #     password=userPW,
    #     host=userHost,
    #     port=userPort,
    #     database="task_listing",
    # )

    cursor = connection.cursor()

except mariadb.Error as error:
    print(f"Error connecting to MariaDB Platform: {error}")
    sys.exit(1)
