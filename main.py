import mysql.connector
from mysql.connector import Error
import logging
import pandas as pd

logging.basicConfig(filename='logfile.log', encoding='utf-8', level=logging.DEBUG)

def get_db_connection():
    """get_db_connection uses the create_engine module from sqlalchemy

        Returns:
            connection to the mysql database 'ticket_sales'

        Exceptions are logged.
    """
    connection = None
    try:
        connection = mysql.connector.connect(user = 'root', password = 'password',
                                             host = 'localhost', database = 'ticket_sales')
    except Exception as error:
        logging.info(error)
        print(error)
    return connection


def write_to_table(connection, file):
    """write_to_table reads in the csv from a filepath and writes to the connected MySQL server
       Pandas is used to read the csv, which stores the contents in a DataFrame
       From there, the cursor object is utilized to perform SQL queries

        Inputs:
            connection: engine created using create_engine module
            file: the file path that contains the csv to read

        Objects:
            labels: keys for the csv table
            dtypes: dictionary with data types for read_csv function
            prase_dates: used to convert str to date type
    """
    labels = [
        'ticket_id', 'trans_date', 'event_id', 'event_name', 'event_date',
        'event_type', 'event_city', 'customer_id', 'price', 'num_tickets'
    ]

    dtypes = {
        'ticket_id': int,
        'trans_date': str,
        'event_id': int,
        'event_name': str,
        'event_date': str,
        'event_type': str,
        'event_city': str,
        'customer_id': int,
        'price': float,
        'num_tickets': int
    }

    parse_dates = ['trans_date', 'event_date']

    df = pd.read_csv(file, header=None, names=labels, dtype=dtypes, 
                     parse_dates=parse_dates, index_col=False, delimiter=',')

    create_statement = """
        CREATE TABLE IF NOT EXISTS third_party_sales(
            ticket_id SMALLINT(255) NOT NULL AUTO_INCREMENT PRIMARY KEY, trans_date DATE,
            event_id SMALLINT(255) NOT NULL, event_name VARCHAR(255), event_date DATE,
            event_type VARCHAR(255), event_city VARCHAR(255), customer_id SMALLINT(255) NOT NULL,
            price FLOAT(255, 2), num_tickets TINYINT(255))
        """

    insert_statement = 'INSERT INTO third_party_sales VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    if connection.is_connected(): # Runs code only if there is a valid connection
        try: # This block connects to MySQL database and creates table
            cursor = connection.cursor()
            cursor.execute(create_statement)
        except Error:
            logging.info(Error)
        else:
            connection.commit()
            print("Table in MySQL created successfully!")
        
        try: # This block inserts into the MySQL table created
            for i,row in df.iterrows():
                cursor.execute(insert_statement, tuple(row))
        except Error:
            logging.info(Error)
        else:
            connection.commit()
            print("Table updated successfully!")


def query_popular_events(connection):
    """Queries the third_party_sales table to search for the most popular event"""

    query = 'SELECT event_name FROM third_party_sales GROUP BY event_id, event_name LIMIT 3'

    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()
        
    print("Here are the most popular tickets in the past month:")
    
    for tup in record: # Iterate through the info fetched from the cursor object to print
        for letter in tup:
            letter.replace("(',)", "") # makes information presentable
            print(letter)


def most_ticket_sales(connection):
    """Queries the third_party_sales table to find the event with the most tickets sold"""

    query = """
        SELECT event_name, SUM(num_tickets) AS total_tickets FROM third_party_sales
        GROUP BY num_tickets, event_name ORDER BY total_tickets DESC LIMIT 3;
    """
    
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(query)
        record = cursor.fetchall()

        print('Here are the events that have the most tickets sold from the third party vendor:')

        for tup in record: # Iterate through the fetched cursor info to print
            for letter in tup:
                str(letter).replace("(',)Decimal.", "") # Makes information presentable
                print(letter)

if __name__ == '__main__':
    file = 'third_party_sales_1.csv'
    connection = get_db_connection()

    print("Please choose on of the following:")
    choice = int(input("""
        1) Update the third_party_sales table
        2) Query the popular events
        3) Get the event with the most tickets sold
        4) Exit
        """)
    )

    if choice == 1:
        write_to_table(connection, file)
    elif choice == 2:
        query_popular_events(connection)
    elif choice == 3:
        most_ticket_sales(connection)
    else:
        print("Exiting...")

    connection.close()
