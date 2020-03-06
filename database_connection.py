import sqlite3
from sqlite3 import Error
from exercises import ExerciseDirectory
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
    INSERT INTO exercises(ExerciseName, ID, ExerciseGroup, SpecificGroup, ExerciseType, Probability)
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
    INSERT INTO user_data(UserID, ExerciseName, OneRepMax, LastUsed, BodyWeight)
    VALUES (?,?,?,?,?)
    '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid


def update_user_config(conn, data):
    """
    The User can update their workout preferences, bodyweight, bodyfat etc using this.
    :param conn:
    :param data:
    :return:
    """
    sql = '''
    INSERT INTO user_config(UpdateTime, UserID, WorkoutTypeMain, WorkoutTypeSec, WarmUpTime, CoolDownTime, WarmUpMain,
                            MonEx, TueEx, WedEx, ThuEx, FriEx, SatEx, SunEx, Mon, Tue, Wed, Thu, Fri, Sat, Sun,
                            BodyWeight, BodyFat)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid


def load_user_config(conn, user_id):
    """
    :param conn:
    :param user_id:
    :return:
    """
    sql = f'''
    SELECT * from user_config
    where UserID = '{user_id}'
    and UpdateTime = (SELECT MAX(UpdateTime) FROM user_config WHERE UserID = '{user_id}')
    '''
    result = pandas.read_sql_query(sql, conn)
    result.drop('UpdateTime', axis=1, inplace=True)
    # We are only returning 1 row hence we are gonna return a series instead of a DataFrame
    return result.iloc[0]


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
    SELECT * from exercises ex
    JOIN user_data ud on ex.ExerciseName=nud.ExerciseName
    {"--" if user_id is None else ""} WHERE nud.UserID = '{user_id}'
    {"--" if exercise_group is None else ""} {"WHERE " if user_id is None else "AND "} 
        ex.ExerciseGroup in ('{exercise_group if exercise_group is not None else ""}')
    {"--" if specific_group is None else ""} {"WHERE " if user_id is None and exercise_group is None else "AND "} 
        ex.SpecificGroup in ('{specific_group if specific_group is not None else ""}')
    ORDER BY ud.LastUsed DESC
    ) as tmp
    GROUP BY ExerciseName {"--" if user_id is not None else ""}, tmp.UserID
    '''
    cur = conn.cursor()
    cur.execute(sql)
    result = pandas.read_sql_query(sql, conn)
    return result.drop('ExerciseName:1', axis=1)


def setup_connection(database=r"C:\Users\Gabor\PycharmProjects\gym\exercises_db\exercises.db"):
    return create_connection(database)


DB_CONN = setup_connection()
