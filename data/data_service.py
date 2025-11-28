import sqlite3
from typing import Any, Dict, List

# Package
import mariadb
from termcolor import colored

# Custom
import models.globals
from models.log_level import LogLevel


class DataService:
    """Service for CRUD operations on the primary database and secrets database"""

    def get_all_rows(sql_statement: str):
        """Accepts a SQL SELECT * statement and returns a JSON like list of results"""
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(sql_statement)
            data = cursor.fetchall()
            return DataService.translate_many_to_json_like(cursor, data)
        except mariadb.Error as e:
            print(colored(f"Get All Error: {e}"), LogLevel.ERROR_MESSAGE.value)
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
            print(colored(f"Get One Error: {e}"), LogLevel.ERROR_MESSAGE.value)
            DataService.handle_reconnect_error(e)

    def insert_record(sql_statement: str, data: tuple[Any]):
        """Accepts a SQL INSERT statement and data for database record insertion"""
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(sql_statement, data)
            models.globals._connectionPrimary.commit()
        except mariadb.Error as e:
            print(colored(f"Insert Error: {e}", LogLevel.ERROR_MESSAGE.value))
            DataService.handle_reconnect_error(e)

    def update_record(sql_statement: str, data: tuple[Any]):
        """Accepts a SQL UPDATE statement and data for database record updates"""
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(sql_statement, data)
            models.globals._connectionPrimary.commit()
        except mariadb.Error as e:
            print(colored(f"Update Error: {e}", LogLevel.ERROR_MESSAGE.value))
            DataService.handle_reconnect_error(e)

    def delete_record(sql_statement: str, data: tuple[Any]):
        """Accepts a SQL DELETE statement and data for database record deletion"""
        try:
            cursor = models.globals._connectionPrimary.cursor()
            cursor.execute(sql_statement, data)
            models.globals._connectionPrimary.commit()
        except mariadb.Error as e:
            print(colored(f"Delete Error: {e}", LogLevel.ERROR_MESSAGE.value))
            DataService.handle_reconnect_error(e)

    # --- --- --- --- --- SECRET HANDLERS --- --- --- --- --- #

    def get_all_secrets():
        """Get all secrets from the secrets.db"""
        try:
            cursor = models.globals._connectionSecrets.cursor()
            auth_creds_tuple = cursor.execute("SELECT * FROM secrets").fetchall()
            auth_dict = dict(auth_creds_tuple)
            return auth_dict
        except sqlite3.Error as e:
            print(
                colored(f"Error in fetching secrets: {e}", LogLevel.ERROR_MESSAGE.value)
            )

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
            print(colored("Tokens Refreshed", LogLevel.SUCCESS_MESSAGE.value))
        except sqlite3.Error as e:
            print(
                colored(
                    f"Error in updating Bot tokens: {e}", LogLevel.ERROR_MESSAGE.value
                )
            )

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
