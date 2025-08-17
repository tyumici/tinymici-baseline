import mariadb
import os
import sqlite3
import sys
import schedule
import threading
import time
import mysql.connector
from mysql.connector import Error
from termcolor import colored
from typing import Any, Dict, List
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

    def connect_primary():
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

    def get_all_data(getString: str):
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(getString)
            data = cursor.fetchall()
            return DataService.translate_many_to_json_like(cursor, data)
        except mariadb.Error as e:
            print(colored(f"Get All Error: {e}"), "red")

    def get_one_data(getString: str):
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(getString)
            data = cursor.fetchone()
            if data:
                return DataService.translate_single_to_json_like(cursor, data)
            else:
                return None
        except mariadb.Error as e:
            print(colored(f"Get One Error: {e}"), "red")
            DataService.handle_reconnect_error(e)

    def insert_record(insertString: str, data: tuple[Any]):
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(insertString, data)
            models.globals._connectionPrimary.commit()
        except mariadb.Error as e:
            print(colored(f"Insert Error: {e}", "red"))
            DataService.handle_reconnect_error(e)

    def update_record(updateString: str, data: tuple[Any]):
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(updateString, data)
            models.globals._connectionPrimary.commit()
        except mariadb.Error as e:
            print(colored(f"Update Error: {e}", "red"))
            DataService.handle_reconnect_error(e)

    def delete_record(deleteString: str, data: tuple[Any]):
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(deleteString, data)
            models.globals._connectionPrimary.commit()
        except mariadb.Error as e:
            print(colored(f"Delete Error: {e}", "red"))
            DataService.handle_reconnect_error(e)

    def handle_reconnect_error(e):
        if "Server has gone away" in str(e):
            models.globals._connectionPrimary = DataService.reconnect_primary(
                models.globals._connectionPrimary
            )

    # --- --- --- --- --- SECRET HANDLERS --- --- --- --- --- #

    def connect_secrets():
        try:
            models.globals._connectionSecrets = sqlite3.connect("./secrets.db")
            models.globals._connectionSecrets.autocommit = True
            print(colored("Connected to secrets db on SQLite", "green"))
            return models.globals._connectionSecrets.cursor()
        except sqlite3.Error as e:
            print(f"Error in connecting to secrets: {e}")

    def get_all_secrets():
        try:
            cursor = models.globals._connectionSecrets.cursor()
            auth_creds_tuple = cursor.execute("SELECT * FROM secrets").fetchall()
            auth_dict = dict(auth_creds_tuple)
            return auth_dict
        except sqlite3.Error as e:
            print(f"Error in fetching secrets: {e}")

    def update_bot_tokens(token: str, refresh_token: str):
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
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in data]
        return result

    def translate_single_to_json_like(cursor, data) -> List[Dict[str, Any]]:
        columns = [column[0] for column in cursor.description]
        result = dict(zip(columns, data))
        return result
