import datetime
import sqlite3

from database_connection import add_user_data, setup_connection
from exercises import ExerciseDirectory
from orm import avg_orm, adjusted_bench_press, adjusted_deadlift, adjusted_squat


def update_orms(_conn, default_userid=None, default_bodyweight=None, default_weight=0, default_reps=1,
                _exercises=ExerciseDirectory.items()):
    with _conn:
        for group in _exercises:
            for ex in group:
                # Selecting the One Rep Max Calculator
                if "Squat" in ex.ExerciseName:
                    default_orm_calculator = adjusted_squat
                elif "Deadlift" in ex.ExerciseName:
                    default_orm_calculator = adjusted_deadlift
                elif "Bench" in ex.ExerciseName:
                    default_orm_calculator = adjusted_bench_press
                else:
                    default_orm_calculator = avg_orm
                # We don't need this input is the User ID is provided
                if default_userid is None:
                    default_userid = int(input("Enter your User ID: ") or default_userid)
                # We don't need this input is Body Weight is provided
                if default_bodyweight is None:
                    default_bodyweight = int(input("Enter your body weight: ") or default_bodyweight)

                default_weight = int(
                    input(f"Enter the max weight lifted for {ex.ExerciseName}: ") or default_weight)
                default_reps = int(
                    input(f"Enter the max reps for the weight lifted for {ex.ExerciseName}: ") or default_reps)
                orm = default_orm_calculator(default_weight, default_reps)
                try:
                    data = [default_userid, ex.ExerciseName, orm, datetime.date.today(), default_bodyweight]
                    accept = int(
                        input(f"About to enter the following into the Database: {data}, please confirm: ", ) or 1)
                    if not accept:
                        continue
                    add_user_data(conn, data)
                except sqlite3.IntegrityError:
                    print(f'Value is already entered {data}')


if __name__ == '__main__':
    conn = setup_connection()
    update_orms(conn, 'Gabor', 109, 0, 1, list(ExerciseDirectory.values())[-4:])