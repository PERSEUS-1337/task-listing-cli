# Task Listing CLI

## Initial Setup

1. Create a Python virtual environment.

```sh
python -m venv venv
```

2. Activate the virtual environment.

```sh
. venv/Scripts/activate
```

3. Install the program dependencies in the virtual environment.

```sh
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory containing your database credentials assigned to the following variables:

```sh
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_hostname
DB_PORT=your_port
```

If you don't know the hostname and port number, connect to the database and execute the following SQL command:

```mysql
SHOW variables WHERE `variable_name` IN ("hostname", "port");
```

5. Setup the program database with the help of a shell script.

```sh
. setup/database_setup.sh
```

6. Run the application.

```sh
python app.py
```

## Rerun

If you have done the initial setup before, you can rerun the application again by simply doing steps 2 and 6.
