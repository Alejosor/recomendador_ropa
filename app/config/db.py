import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="futbolera",
        user="futbolera_user",
        password="LVlPwRImzV7FrkrCWjOpjuhpGAInEBz4",
        host="dpg-d0t7je49c44c7396r900-a.oregon-postgres.render.com",
        port="5432"
    )
