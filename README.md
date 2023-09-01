## Installation

### Python Django 
1. Create a virtual environment
   Run the following command to create a virtual environment named "env" (you can replace "env" with your preferred name):

```bash
python -m venv env
```

2. Activate the Virtual Environment:
   To activate the virtual environment, run:

```bash
source env/bin/activate
```

3. Create .env file

```bash
SECRET_KEY=
USER=
PASSWORD= 
EMAIL=
EMAIL_PASSWORD=
EMAIL_ADMIN=

```


4. Install Packages and Run Your Project:
   After activating the virtual environment, you can install packages and run your project as usual:

```bash
pip install -r requirements.txt
chmod +x run_server.sh
.\run_server.sh
```
or
```bash
nohup ./run_server.sh 2>&1 &
```


5. Deactivate the Virtual Environment:
   When you're done working in the virtual environment, you can deactivate it using the following command:

```bash
deactivate
```

The virtual environment will be deactivated, and you'll return to the regular Command Prompt.

### To Setup MYSQL Database 

1. Install the MySQL client library for Python to connect to the  MySQL database. You can do this using:

```bash
pip install mysqlclient
```

2. Create a MySQL Database and User:

Once MySQL is installed, you can log in to the MySQL shell:

```bash
sudo mysql
```
3. Inside the MySQL shell, you can create a database and a user for your Django project:

```bash
CREATE DATABASE yourdbname;
CREATE USER 'yourdbuser'@'localhost' IDENTIFIED BY 'yourdbpassword';
GRANT ALL PRIVILEGES ON yourdbname.* TO 'yourdbuser'@'localhost';
FLUSH PRIVILEGES;
```

### Run Migrations:

After configuring the database settings, you need to apply migrations to create the necessary database tables:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
