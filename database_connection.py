import sqlite3
from sqlite3 import Error
from exercises import ExerciseDirectory
import datetime
import pandas


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def add_exercise(conn, exercise):
    """
    :param conn:
    :param exercise:
    :return:
    """
    sql = '''
    INSERT INTO n_exercises(ExerciseName, ID, ExerciseGroup, SpecificGroup, ExerciseType, Probability)
    VALUES (?,?,?,?,?,?)
    '''
    cur = conn.cursor()
    cur.execute(sql, exercise)
    return cur.lastrowid


def add_user_data(conn, data):
    """
    :param conn:
    :param data:
    :return:
    """
    sql = '''
    INSERT INTO n_user_data(UserID, ExerciseName, OneRepMax, LastUsed, BodyWeight)
    VALUES (?,?,?,?,?)
    '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid


def load_data(conn, user_id=None):
    """
    :param conn:
    :param extras:
    :return:
    """
    sql = '''
    SELECT * FROM n_user_data
    '''
    sql = f'''
    SELECT DISTINCT * from n_exercises
    JOIN n_user_data on n_exercises.ExerciseName=n_user_data.ExerciseName
    WHERE n_user_data.LastUsed =    (
                                    select MAX(LastUsed)
                                    from n_user_data 
                                    {"--" if user_id is None else ""} where UserID = '{user_id}'
                                    )
    {"--" if user_id is None else ""} AND n_user_data.UserID = '{user_id}'
    '''
    cur = conn.cursor()
    cur.execute(sql)
    return pandas.read_sql_query(sql, conn)


def main():
    database = r"C:\Users\Gabor\PycharmProjects\gym\exercises_db\exercises.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        for group in ExerciseDirectory.items():
            for ex in group[1]:
                values = [
                    ex.ExerciseName,
                    ex.ID,
                    ex.ExerciseGroup,
                    ex.SpecificGroup,
                    ex.ExerciseType,
                    ex.Probability]
                values = [str(el) for el in values]
                # print(f"Currently adding {values} to our database")
                try:
                    add_exercise(conn, values)
                except sqlite3.IntegrityError:
                    pass
                    # print(f'Value is already entered {values}')
    with conn:
        try:
            data = ['PI', 'Deadlifts', 170, datetime.date(2020, 2, 18), 109]
            # print(data)
            add_user_data(conn, data)
        except sqlite3.IntegrityError:
            print(f'Value is already entered {data}')

    with conn:
        print(load_data(conn, user_id='Gabor'))


if __name__ == '__main__':
    main()
