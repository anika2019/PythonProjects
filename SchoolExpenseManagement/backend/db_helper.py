import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
import logging

# Configure custom logger
logger = logging.getLogger('db_helper')
logger.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler('server.log')
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_db_connection():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='expense_manager',
                                             user='root',
                                             password='Aky@4939552e')
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"Inserting expense: {expense_date}, {amount}, {category}, {notes}")
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO expenses (amount, category, expense_date, notes) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (expense_date, amount, category, notes))
            connection.commit()
            print("Expense added successfully")
        except Error as e:
            print("Error adding expense:", e)
        finally:
            cursor.close()
            connection.close()

def get_expenses():
    logger.info("Fetching all expenses")
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM expenses")
            expenses = cursor.fetchall()
            return expenses
        except Error as e:
            print("Error fetching expenses:", e)
            return []
        finally:
            cursor.close()
            connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"Fetching expenses for date: {expense_date}")
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM expenses WHERE expense_date = %s"
            cursor.execute(query, (expense_date,))
            expenses = cursor.fetchall()
            return expenses
        except Error as e:
            print("Error fetching expenses for date:", e)
            return []
        finally:
            cursor.close()
            connection.close()

def delete_expenses_for_date(expense_date):
    logger.info(f"Deleting expenses for date: {expense_date}")
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM expenses WHERE expense_date = %s"
            cursor.execute(query, (expense_date,))
            connection.commit()
            print("Expenses deleted successfully for date:", expense_date)
        except Error as e:
            print("Error deleting expenses for date:", e)
        finally:
            cursor.close()
            connection.close()
  


def fetch_expenses_by_date(start_date, end_date):
    logger.info(f"Fetching expenses for date range: {start_date} to {end_date}")
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT category, SUM(amount) as total_amount FROM expenses WHERE expense_date between %s and %s GROUP BY category"
            
            cursor.execute(query, (start_date, end_date))
            summary = cursor.fetchall()
            return summary
        except Error as e:
            print("Error fetching summary:", e)
            return []
        finally:
            cursor.close()
            connection.close()

def main():
    

    print("\nFetching summary for given dates range:")
    summary = fetch_expenses_by_date("2024-08-01", "2024-09-30")
    for item in summary:
        print(item)
    


if __name__ == "__main__":
    main()
