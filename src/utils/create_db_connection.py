import snowflake.connector
import os
from dotenv import load_dotenv


def connect_to_snowflake():
    load_dotenv(dotenv_path=r"..\..\.env", override=True)
    user = os.environ.get('user')
    password = os.environ.get('password')
    account = os.environ.get('account')
    warehouse = os.environ.get('warehouse')
    database = os.environ.get('database')
    schema = os.environ.get('schema')
    role = os.environ.get('role')

    try:
        conn = snowflake.connector.connect(
            user = user,
            password = password,
            account = account,
            warehouse = warehouse,
            database = database,
            schema = schema,
            role = role
            )

        return conn
    except Exception as e:
        print(f"Error! Could not connect to Snowflake database: {e}")
