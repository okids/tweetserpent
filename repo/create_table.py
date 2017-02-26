from util import create_sql_connection

connection = create_sql_connection()

try:
    with connection.cursor() as cursor:
        # Create table as per requirement
        cursor.execute("DROP TABLE IF EXISTS USER_COUNTER")

        sql = """CREATE TABLE USER_COUNTER (
           USER_NAME  VARCHAR(20) NOT NULL,
           USER_ID INT,
           COUNTER INT )"""
        cursor.execute(sql)

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS WORD_COUNTER")
        sql = """CREATE TABLE WORD_COUNTER (
                   WORD  VARCHAR(20) NOT NULL,
                   COUNTER INT )"""
        cursor.execute(sql)

    connection.commit()

    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS SENTIMENT_COUNTER")
        sql = """CREATE TABLE SENTIMENT_COUNTER (
                   OBJECT VARCHAR(20) NOT NULL,
                   NEGATIVE_COUNTER INT,
                   NEUTRAL_COUNTER INT,
                   POSITIVE_COUNTER INT )"""
        cursor.execute(sql)

    connection.commit()


finally:
    connection.close()