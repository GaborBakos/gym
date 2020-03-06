import datetime
import sqlite3

from database_connection import add_user_data, add_exercise, update_user_config, DB_CONN
from exercises import ExerciseDirectory
from orm import avg_orm, adjusted_bench_press, adjusted_deadlift, adjusted_squat


class UserConfig:
    def __init__(self, user_id, workout_type_main, workout_type_sec, warmup_time, cool_down_time, warmup_main,
                 mon_ex, tue_ex, wed_ex, thu_ex, fri_ex, sat_ex, sun_ex, mon, tue, wed, thu, fri, sat, sun,
                 body_weight, body_fat):
        self.user_id = user_id
        self.workout_type_main = workout_type_main
        self.workout_type_sec = workout_type_sec
        self.warmup_time = warmup_time
        self.cool_down_time = cool_down_time
        self.warmup_main = warmup_main
        self.mon_ex = mon_ex
        self.tue_ex = tue_ex
        self.wed_ex = wed_ex
        self.thu_ex = thu_ex
        self.fri_ex = fri_ex
        self.sat_ex = sat_ex
        self.sun_ex = sun_ex
        self.mon = mon
        self.tue = tue
        self.wed = wed
        self.thu = thu
        self.fri = fri
        self.sat = sat
        self.sun = sun
        self.body_weight = body_weight
        self.body_fat = body_fat

    def __repr__(self):
        return f'User ID: {self.user_id}'


def update_orms(db_conn, default_userid=None, default_bodyweight=None, default_weight=0, default_reps=1,
                _exercises=ExerciseDirectory.items()):
    with db_conn as db:
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
                    add_user_data(db, data)
                except sqlite3.IntegrityError:
                    print(f'Value is already entered {data}')


def update_exercise_list(db_conn, exercise_directory):
    with db_conn as db:
        for group in exercise_directory:
            for exercise in group[1]:
                values = [
                    exercise.ExerciseName,
                    exercise.ID,
                    exercise.SpecificGroup,
                    exercise.ExerciseType,
                    exercise.Probability
                ]
                values = [str(el) for el in values]
                print("Currently adding {values} to our database.")
                try:
                    add_exercise(db, values)
                except sqlite3.IntegrityError:
                    print(f"Row is already present in our database.")


def update_single_exercise(db_conn, user_name, exercise_name, w, bw, date=None):
    if date is None:
        date = datetime.datetime.today()
    with db_conn as db:
        data = [user_name, exercise_name, w, date, bw]
        try:
            add_user_data(db, data)
        except sqlite3.IntegrityError:
            print("This value has already been inserted to the database")


def update_user_configuration(db_conn, uc):
    with db_conn as db:
        data = [datetime.datetime.now(),
                uc.user_id, uc.wokrout_type_main, uc.workout_type_sec, uc.warmup_time, uc.cool_down_time,
                uc.warmup_main, uc.mon_ex, uc.tue_ex, uc.wed_ex, uc.thu_ex, uc.fri_ex, uc.sat_ex, uc.sun_ex,
                uc.mon, uc.tue, uc.wed, uc.thu, uc.fri, uc.sat, uc.sun, uc.body_weight, uc.body_fat]
        try:
            update_user_config(db, data)
        except sqlite3.IntegrityError:
            print("This value has already been inserted to the database")


from exercises import WorkoutType, ExerciseGroup
if __name__ == '__main__':
    # update_orms(DB_CONN, 'Gabor', 109, 0, 1, list(ExerciseDirectory.values())[-4:])
    user_config = UserConfig('Gabor', str(WorkoutType.STRENGTH), str(WorkoutType.MUSCLE), 15, 15, 1,
                             str(ExerciseGroup.CHEST), str(ExerciseGroup.BACK), str(ExerciseGroup.REST),
                             str(ExerciseGroup.DEADLIFT), str(ExerciseGroup.SHOULDER), str(ExerciseGroup.BACK),
                             str(ExerciseGroup.SQUAT), 90, 90, 45, 90, 90, 120, 120, 109, 25.5)
    update_user_configuration(DB_CONN, user_config)
