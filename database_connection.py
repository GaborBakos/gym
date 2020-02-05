import sqlite3
from sqlite3 import Error
from exercises import ExerciseDirectory

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
    INSERT INTO exercises(ExerciseName, NumSets, NumReps, Weights, TimeRequired, RestTimer, ExerciseType,
                          ExerciseGroup, Probability, LastUsed)
    VALUES (?,?,?,?,?,?,?,?,?,?)
    '''
    cur = conn.cursor()
    cur.execute(sql, exercise)
    return cur.lastrowid


def main():
    database = r"C:\Users\Gabor\PycharmProjects\gym\exercises_db\exercises.db"

    # create a database connection
    conn = create_connection(database)
    with conn:

        # # create a new project
        # project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
        # project_id = create_project(conn, project)
        #
        # # tasks
        # task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        # task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
        #
        # # create tasks
        # create_task(conn, task_1)
        # create_task(conn, task_2)
        for group in ExerciseDirectory.items():
            for ex in group[1]:
                print(f"Currently adding {ex} to our database")
                add_exercise(conn, (str(el) for el in vars(ex).values()))
        # TODO correct types

if __name__ == '__main__':
    main()
