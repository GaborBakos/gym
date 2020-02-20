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


def load_data(conn, user_id=None, exercise_group=None, specific_group=None):
    """
    :param conn:
    :param extras:
    :return:
    """

    if exercise_group is not None:
        exercise_group = '\', \''.join(exercise_group)
    if specific_group is not None:
        specific_group = '\', \''.join(specific_group)
    sql = f'''
    SELECT * from (
    SELECT * from n_exercises ne
    JOIN n_user_data nud on ne.ExerciseName=nud.ExerciseName
    {"--" if user_id is None else ""} WHERE nud.UserID = '{user_id}'
    {"--" if exercise_group is None else ""} {"WHERE " if user_id is None else "AND "} ne.ExerciseGroup in ('{exercise_group if exercise_group is not None else ""}')
    {"--" if specific_group is None else ""} {"WHERE " if user_id is None and exercise_group is None else "AND "} ne.SpecificGroup in ('{specific_group if specific_group is not None else ""}')
    ORDER BY nud.LastUsed DESC
    ) as tmp
    GROUP BY ExerciseName {"--" if user_id is not None else ""}, tmp.UserID
    '''
    cur = conn.cursor()
    cur.execute(sql)
    result = pandas.read_sql_query(sql, conn)
    return result.drop('ExerciseName:1', axis=1)


def setup_connection(database=r"C:\Users\Gabor\PycharmProjects\gym\exercises_db\exercises.db"):
    return create_connection(database)


def main():
    # create a database connection
    conn = setup_connection()
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
        for group in ExerciseDirectory.items():
            for ex in group[1]:
                try:
                    data = ['Gabor', ex.ExerciseName, 100, datetime.date(2020, 2, 18), 109]
                    add_user_data(conn, data)
                except sqlite3.IntegrityError:
                    print(f'Value is already entered {data}')

    with conn:
        print(load_data(conn, user_id=None, specific_group=['ExerciseGroup.SQUAT', 'ExerciseGroup.DEADLIFT']))


if __name__ == '__main__':
    main()
