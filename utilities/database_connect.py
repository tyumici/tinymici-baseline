import os
import sys
import sqlite3
import threading
import time

# Package
import schedule
import mariadb
import mysql.connector
from mysql.connector import Error
from termcolor import colored

# Custom
import models.globals
from models.log_level import LogLevel

# --- --- --- --- --- RECONNECT HANDLERS --- --- --- --- --- #


class DatabaseConnector:

    def reconnect_db_job():
        """Simple job to reconnect the primary database"""
        models.globals._connectionPrimary = DatabaseConnector.reconnect_primary(
            models.globals._connectionPrimary
        )
        print(
            colored(
                "A scheduled DB reconnect has occurred", LogLevel.CONNECTION_MESSAGE.value
            )
        )

    schedule.every(4).hours.do(reconnect_db_job)  # run database reconnect every 4 hours

    def run_scheduler():
        print(colored("DB Reconnect Schedule Started", LogLevel.CONNECTION_MESSAGE.value))
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_scheduler, daemon=True).start()

    def reconnect_primary(connection):
        """Ping the Database and reconnect on ping failure"""
        while True:
            try:
                connection.ping(reconnect=True)
                print(colored("MariaDB PING succeeded", LogLevel.SUCCESS_MESSAGE.value))
                break
            except Error as e:
                print(
                    colored(
                        f"MariaDB Connection lost. Attempting to reconnect: {e}",
                        LogLevel.SUCCESS_MESSAGE.value,
                    )
                )
                time.sleep(10)
                connection = DatabaseConnector.connect_primary()

        return connection

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
                print(
                    colored(
                        "Connected to MariaDB on test DB",
                        LogLevel.SUCCESS_MESSAGE.value,
                    )
                )
                return models.globals._connectionPrimary
        except mariadb.Error as e:
            print(
                colored(
                    f"Error connecting to MariaDB Platform: {e}",
                    LogLevel.ERROR_MESSAGE.value,
                )
            )
            sys.exit(1)

    def handle_reconnect_error(e):
        """Simple disconnect handler for use on DB connection error"""
        if "Server has gone away" in str(e):
            models.globals._connectionPrimary = DatabaseConnector.reconnect_primary(
                models.globals._connectionPrimary
            )

    def connect_secrets():
        """Connect to the local sqlite secrets.db and assign the global ._connectionSecrets"""
        try:
            models.globals._connectionSecrets = sqlite3.connect("./secrets.db")
            models.globals._connectionSecrets.autocommit = True
            print(
                colored(
                    "Connected to secrets db on SQLite", LogLevel.SUCCESS_MESSAGE.value
                )
            )
            return models.globals._connectionSecrets.cursor()
        except sqlite3.Error as e:
            print(
                colored(
                    f"Error in connecting to secrets: {e}", LogLevel.ERROR_MESSAGE.value
                )
            )
