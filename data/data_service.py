import os
import sys
import sqlite3
import threading
import time
from typing import Any, Dict, List

# Package
import schedule
import mariadb
import mysql.connector
from mysql.connector import Error
from termcolor import colored

# Custom
import models.globals

# --- --- --- --- --- RECONNECT HANDLERS --- --- --- --- --- #


def reconnect_db_job():
    """Simple job to reconnect the primary database"""
    models.globals._connectionPrimary = DataService.reconnect_primary(
        models.globals._connectionPrimary
    )
    print(colored("A scheduled DB reconnect has occurred", "green"))


schedule.every(4).hours.do(reconnect_db_job)  # run database reconnect every 4 hours


def run_scheduler():
    print(colored("DB Reconnect Schedule Started", "yellow"))
    while True:
        schedule.run_pending()
        time.sleep(1)


threading.Thread(target=run_scheduler, daemon=True).start()


class DataService:
    """Service for CRUD operations on the primary database and secrets database"""

    def connect_primary():
        """Connect to the primary database and assign the global _connectedPrimary connection"""
        try:
            models.globals._connectionPrimary = mysql.connector.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database=os.getenv("DB_NAME"),
            )
            if models.globals._connectionPrimary.is_connected():
                print(colored("Connected to MariaDB on test DB", "green"))
                return models.globals._connectionPrimary
        except mariadb.Error as e:
            print(colored(f"Error connecting to MariaDB Platform: {e}", "red"))
            sys.exit(1)

    def reconnect_primary(connection):
        """Ping the Database and reconnect on ping failure"""
        while True:
            try:
                connection.ping(reconnect=True)
                print(colored("MariaDB PING succeeded", "green"))
                break
            except Error as e:
                print(
                    colored(
                        f"MariaDB Connection lost. Attempting to reconnect: {e}",
                        "yellow",
                    )
                )
                time.sleep(10)
                connection = DataService.connect_primary()

        return connection

    def get_all_rows(sql_statement: str):
        """Accepts a SQL SELECT * statement and returns a JSON like list of results"""
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(sql_statement)
            data = cursor.fetchall()
            return DataService.translate_many_to_json_like(cursor, data)
        except mariadb.Error as e:
            print(colored(f"Get All Error: {e}"), "red")
            DataService.handle_reconnect_error(e)

    def get_single_row(sql_statement: str):
        """
        Accepts a SQL SELECT that would return one row
        
        ex: using a WHERE id statement
        """
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(sql_statement)
            data = cursor.fetchone()
            if data:
                return DataService.translate_single_to_json_like(cursor, data)
            else:
                return None
        except mariadb.Error as e:
            print(colored(f"Get One Error: {e}"), "red")
            DataService.handle_reconnect_error(e)

    def insert_record(sql_statement: str, data: tuple[Any]):
        """Accepts a SQL INSERT statement and data for database record insertion"""
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(sql_statement, data)
            models.globals._connectionPrimary.commit()
        except mariadb.Error as e:
            print(colored(f"Insert Error: {e}", "red"))
            DataService.handle_reconnect_error(e)

    def update_record(sql_statement: str, data: tuple[Any]):
        """Accepts a SQL UPDATE statement and data for database record updates"""
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(sql_statement, data)
            models.globals._connectionPrimary.commit()
        except mariadb.Error as e:
            print(colored(f"Update Error: {e}", "red"))
            DataService.handle_reconnect_error(e)

    def delete_record(sql_statement: str, data: tuple[Any]):
        """Accepts a SQL DELETE statement and data for database record deletion"""
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(sql_statement, data)
            models.globals._connectionPrimary.commit()
        except mariadb.Error as e:
            print(colored(f"Delete Error: {e}", "red"))
            DataService.handle_reconnect_error(e)

    def handle_reconnect_error(e):
        """Simple disconnect handler for use on DB connection error"""
        if "Server has gone away" in str(e):
            models.globals._connectionPrimary = DataService.reconnect_primary(
                models.globals._connectionPrimary
            )

    # --- --- --- --- --- SECRET HANDLERS --- --- --- --- --- #

    def connect_secrets():
        """Connect to the local sqlite secrets.db and assign the global ._connectionSecrets"""
        try:
            models.globals._connectionSecrets = sqlite3.connect("./secrets.db")
            models.globals._connectionSecrets.autocommit = True
            print(colored("Connected to secrets db on SQLite", "green"))
            return models.globals._connectionSecrets.cursor()
        except sqlite3.Error as e:
            print(f"Error in connecting to secrets: {e}")

    def get_all_secrets():
        """Get all secrets from the secrets.db"""
        try:
            cursor = models.globals._connectionSecrets.cursor()
            auth_creds_tuple = cursor.execute("SELECT * FROM secrets").fetchall()
            auth_dict = dict(auth_creds_tuple)
            return auth_dict
        except sqlite3.Error as e:
            print(f"Error in fetching secrets: {e}")

    def update_bot_tokens(token: str, refresh_token: str):
        """Updates the Bot tokens when the user_refresh function from auth_service.py is called"""
        try:
            models.globals._connectionSecrets.autocommit = True
            cursor = models.globals._connectionSecrets.cursor()
            new_tokens = [
                (token, "BOT_ACCESS_TOKEN"),
                (refresh_token, "BOT_REFRESH_TOKEN"),
            ]
            cursor.executemany(
                "UPDATE SECRETS SET 'VALUE' = ? WHERE 'TYPE' = ?", new_tokens
            )
            print("Tokens Refreshed")
        except sqlite3.Error as e:
            print(f"Error in updating BOT tokens: {e}")

    # --- --- --- --- --- UTILITY --- --- --- --- --- #

    def translate_many_to_json_like(cursor, data) -> List[Dict[str, Any]]:
        """
        Converts row data for multiple rows into a list of dicts
        
        Allows for JSON-like returns of data
        """
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return result

    def translate_single_to_json_like(cursor, data) -> dict:
        """
        Converts row data for a single row into a dict
        
        Allows for JSON-like returns of data
        """
        columns = [column[0] for column in cursor.description]
        result = dict(zip(columns, data))
        return result
