import numpy
import pandas
import copy

from formatter import table_formatter, column_formater, format_df
from exercises import ExerciseRotation, ExerciseType, CollectionExerciseStr
from orm import percentage_of_orm, repetition_percentages_of_orm
from database_connection import setup_connection, load_data, load_user_config

pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
DayList = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
conn = setup_connection()


def _flatten(l):
    return [item for sublist in l for item in sublist]


def _ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(n/10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


def _count_time(l):
    return sum(el[-1] for el in l) + len(l) * 1


def orm_eqv_rep_calculator_for_weight(w, rp_of_orm_dict):
    tmp_dict = {values: keys for keys, values in rp_of_orm_dict.items()}
    return tmp_dict.get(w) or tmp_dict[min(tmp_dict.keys(), key=lambda key: abs(key - w))]


def _round(x, base=2.5):
    return base * round(x/base)


def strength_training(orm, wu=False, orm_calculator=None):
    res = []
    p_of_orm_dict = percentage_of_orm(orm, [0.81, 0.7, 0.6, 0.5])
    if wu:
        times = [1, 1.5, 1.5]
        p_weights = [50, 60, 70]
        reps = [15, 12, 10]
        wu_wrr = [(p_of_orm_dict[w], r, t) for w, r, t in zip(p_weights, reps, times)]
        res.extend(wu_wrr)
    times = [3 for _ in range(5)]
    p_weights = [81 for _ in range(5)]
    wrr = [(p_of_orm_dict[w], 5, t) for w, t in zip(p_weights, times)]
    res.extend(wrr)
    res = [(_round(w), rep, rest) for (w, rep, rest) in res]
    return res


def muscle_building(orm, num_sets=4, wu=False, orm_calculator=None):
    res = []
    p_of_orm_dict = percentage_of_orm(orm, [0.8, 0.7, 0.6, 0.5, 0.4])
    rp_of_orm_dict = repetition_percentages_of_orm(orm, orm_calculator)
    if wu:
        times = [1, 1, 1]
        p_weights = [40, 50, 60]
        reps = [15, 12, 10]
        wu_wrr = [(p_of_orm_dict[w], r, t) for w, r, t in zip(p_weights, reps, times)]
        res.extend(wu_wrr)
    times = [1.5 for _ in range(num_sets)]
    p_weights = [70 for _ in range(num_sets)]
    # w + 10 as with w only it would be a 1 time set, this way we get num reps for 10% harder weights, so can complete
    # hopefully all sets with weight and rep count
    wrr = [(p_of_orm_dict[w], orm_eqv_rep_calculator_for_weight(p_of_orm_dict[w + 10], rp_of_orm_dict), t)
           for w, t in zip(p_weights, times)]
    res.extend(wrr)
    res = [(_round(w), rep, rest) for (w, rep, rest) in res]
    return res


def endurance_training(orm, num_sets=4, wu=False, orm_calculator=None):
    res = []
    p_of_orm_dict = percentage_of_orm(orm, [0.8, 0.7, 0.6, 0.5, 0.4, 0.3])
    rp_of_orm_dict = repetition_percentages_of_orm(orm, orm_calculator)
    if wu:
        times = [1, 1, 1]
        p_weights = [30, 40, 50]
        reps = [15, 15, 15]
        wu_wrr = [(p_of_orm_dict[w], r, t) for w, r, t in zip(p_weights, reps, times)]
        res.extend(wu_wrr)
    times = [1 for _ in range(num_sets)]
    p_weights = [60 for _ in range(num_sets)]
    # w + 10 as with w only it would be a 1 time set, this way we get num reps for 10% harder weights, so can complete
    # hopefully all sets with weight and rep count
    wrr = [(p_of_orm_dict[w], orm_eqv_rep_calculator_for_weight(p_of_orm_dict[w + 10], rp_of_orm_dict), t)
           for w, t in zip(p_weights, times)]
    res.extend(wrr)
    res = [(_round(w), rep, rest) for (w, rep, rest) in res]
    return res
workout_to_func_dict = {'WorkoutType.STRENGTH': strength_training,
                        'WorkoutType.MUSCLE': muscle_building,
                        'WorkoutType.ENDURANCE': endurance_training}

def find_workout_for_day(day):
    """ Finds which workout is on for the given day. """
    return ExerciseRotation[DayList.index(day) % len(ExerciseRotation)]


def filter_main(exercise_df, specific_group, exercise_type=ExerciseType.MAIN):
    return exercise_df[(exercise_df.ExerciseType == str(exercise_type)) &
                       (exercise_df.SpecificGroup == str(specific_group))]


def filter_secondary(exercise_df, specific_group, exercise_type=ExerciseType.SECONDARY):
    return exercise_df[(exercise_df.ExerciseType == str(exercise_type)) &
                       (
                            (exercise_df.SpecificGroup == str(specific_group)) |
                            (exercise_df.SpecificGroup == 'None')
                       )]


def pick_exercise_idx(exercise_list, num_choices):
    """
    Randomly pick an exercise index given the probability distributions provided with them.
    :param exercise_list: The whole list of exercises.
    :param num_choices: The number of choices we want.
    :return: Randomly picked exercises (tilted by their respective probabilities).
    """
    probability_distribution = numpy.array([exercise.Probability
                                            if exercise.Probability is not None
                                            else 0
                                            for idx, exercise in exercise_list.iterrows()])
    probability_distribution /= probability_distribution.sum()
    return int(numpy.random.choice(range(len(exercise_list)), num_choices, p=probability_distribution))


def pick_secondary_exercises(exercise_list, allocated_time, training_type=muscle_building):
    """
    Pick secondary exercises.
    :param exercise_list: The whole list of exercises.
    :param allocated_time: The time we can work with.
    :return: A randomized selection of exercises that should fit into our time limitations and are coherent with our
             main exercise.
    """
    res_secondaries = []
    res_fillers = []
    tmp_ex_list = copy.deepcopy(exercise_list)
    while allocated_time > 0 and len(tmp_ex_list):
        exercise_idx = pick_exercise_idx(tmp_ex_list, 1)
        selected_exercise = copy.deepcopy(tmp_ex_list.iloc[exercise_idx])
        selected_exercise['WRR'] = muscle_building(selected_exercise.OneRepMax, wu=False)
        selected_exercise['TimeRequired'] = _count_time(selected_exercise['WRR'])
        if allocated_time - selected_exercise.TimeRequired < 0:
            tmp_ex_list = tmp_ex_list[tmp_ex_list.ID != selected_exercise.ID]
            continue
        if selected_exercise.ExerciseGroup is not None:
            res_secondaries.append(selected_exercise)
            tmp_ex_list = tmp_ex_list[tmp_ex_list.ID != selected_exercise.ID]
            allocated_time -= selected_exercise.TimeRequired
        else:
            res_fillers.append(selected_exercise)
            tmp_ex_list = tmp_ex_list[tmp_ex_list.ID != selected_exercise.ID]
            allocated_time -= selected_exercise.TimeRequired
    return res_secondaries + res_fillers


def generate_table(day, exercise_list, timed_workout=True):
    """
    Generate a nicely designed table for the workout.
    :param day: Displays the day of the workout.
    :param exercise_list: The list which will be dissected into the table.
    :param timed_workout: Whether to include timings in the table.
    :return: Pandas DataFrame with the workout routine.
    """
    index = []
    max_sets = -numpy.inf
    for ex in exercise_list:
        index.append(ex.ExerciseName)
        if isinstance(ex, pandas.Series):
            max_sets = max(max_sets, len(ex.WRR))
    if ~numpy.isfinite(max_sets):
        max_sets = 0
    index = pandas.Index(index)
    columns = pandas.Index(_flatten([[f"{_ordinal(idx)} Weight", f"{_ordinal(idx)} Reps", f"{_ordinal(idx)} Rest"]
                                    for idx in range(1, max_sets + 1)]), name=day)
    timer_columns = pandas.Index(['Time Alloc'])
    data = numpy.empty((len(exercise_list), max_sets * 3))
    timings = numpy.empty((len(exercise_list), 1), dtype=int)
    for idx, el in enumerate(exercise_list):
        if isinstance(el, pandas.Series):
            weights = [tmp[0] for tmp in el.WRR]
            num_rep = [tmp[1] for tmp in el.WRR]
            rest_ti = [tmp[2] for tmp in el.WRR]
            row = _flatten([[weight, rep, rest] for weight, rep, rest in zip(weights, num_rep, rest_ti)])
            times = [el.TimeRequired]
            while len(row) < max_sets * 3:
                row.extend([None, None, None])
            data[idx, :] = row
            timings[idx, :] = times
        else:
            data[idx, :] = [None for _ in range(max_sets * 3)]
            timings[idx, :] = 15
    timer_df = pandas.DataFrame(timings, index, timer_columns)
    df = pandas.DataFrame(data, index, columns)
    if timed_workout:
        df = pandas.concat([df, timer_df], axis=1)
        df.columns.name = day
    return df


# def generate_workout(day, total_allocated_time, training_type=None, warm_up_time=15, cool_down_time=15, user_config=1):
#     """
#     Generate a coherent workout routine, that is fitted to your needs.
#     :param day: The day determines the workout routine.
#     :param total_allocated_time: How much time is dedicated for the whole training session.
#     :param training_type: tbd
#     :param warm_up_time: tbd
#     :param cool_down_time:  tbd
#     :return: df
#     """
#     print(user_config)
#     if training_type is None:
#         training_type = muscle_building
#     todays_workout = find_workout_for_day(day)
#     collection_workout = CollectionExercise[todays_workout]
#     warm_up_exercise = [(ExerciseDirectory['Warm Up'][1]
#                         if find_workout_for_day(day) == 'Pull'
#                         else ExerciseDirectory['Warm Up'][0])]
#     post_workout_routine = list(ExerciseDirectory['Post Streching'])
#     total_allocated_time -= (warm_up_time + cool_down_time)
#
#     all_exercises = load_data(conn, user_id='Gabor', exercise_group=[str(collection_workout)])
#     if not len(all_exercises):
#         final_list = warm_up_exercise + post_workout_routine
#     else:
#         main_exercises = filter_main(all_exercises, specific_group=todays_workout, exercise_type=ExerciseType.MAIN)
#         selected_main_exercise = copy.deepcopy(main_exercises.iloc[pick_exercise_idx(main_exercises, 1)])
#         selected_main_exercise['WRR'] = training_type(selected_main_exercise.OneRepMax, wu=True)
#         selected_main_exercise['TimeRequired'] = _count_time(selected_main_exercise['WRR'])
#         total_allocated_time -= selected_main_exercise['TimeRequired']
#         secondary_exercises = filter_secondary(all_exercises, specific_group=todays_workout)
#         selected_secondary_exercises = pick_secondary_exercises(secondary_exercises, total_allocated_time)
#         final_list = warm_up_exercise + [selected_main_exercise] + selected_secondary_exercises + post_workout_routine
#     return generate_table(day, final_list)


def generate_weekly_schedule(workout_times_list, cwn):
    for idx, total_time in enumerate(workout_times_list):
        df = generate_workout(DayList[idx], total_time)
        with open(f"C:\\Users\\Gabor\\PycharmProjects\\gym\\week_{cwn}.html", "r+") as f:
            f.write(
                format_df(df, column_style=column_formater, table_style=table_formatter).render().replace("nan", "") +
                '\n\n\n\n\n')
        with open(f"C:\\Users\\Gabor\\Desktop\\THE PLAN\\Gym\\week_{cwn}.html", "a+") as f:
            f.write(
                format_df(df, column_style=column_formater, table_style=table_formatter).render().replace("nan", "") +
                '\n\n\n\n\n')
        print(df)


def generate_workout(day, db_conn, user_cfg):
    """
    Generate a coherent workout routine, that is fitted to your needs.
    :param day:
    :param db_conn:
    :param user_cfg:
    :return:
    """
    total_alloc_time = user_cfg.loc[day]
    training_type_main = workout_to_func_dict[user_cfg.WorkoutTypeMain]
    training_type_sec = workout_to_func_dict[user_cfg.WorkoutTypeSec]

    todays_workout = user_cfg.loc[day + 'Ex']
    collection_workout = CollectionExerciseStr[todays_workout]
    if user_cfg.WarmUpTime and day != 'Wed':
        warm_up_exercise = load_data(db_conn, user_id=user_cfg.UserID, exercise_group=['ExerciseGroup.HIIT'],
                                     specific_group=[collection_workout]).iloc[0]
        warm_up_exercise['WRR'] = [(0, 1, 0)]
        warm_up_exercise['TimeRequired'] = user_cfg.WarmUpTime
        warm_up_exercise = [warm_up_exercise]
    else:
        warm_up_exercise = []
    if user_cfg.CoolDownTime:
        post_workout_exercises = load_data(db_conn, user_id=user_cfg.UserID, exercise_group=['ExerciseGroup.STRETCH'])
        post_workout_exercises = copy.deepcopy(
                                            post_workout_exercises.iloc[pick_exercise_idx(post_workout_exercises, 1)])
        post_workout_exercises['WRR'] = [(0, 1, 0)]
        post_workout_exercises['TimeRequired'] = user_cfg.CoolDownTime
        post_workout_exercises = [post_workout_exercises]
    else:
        post_workout_exercises = []
    total_alloc_time -= (user_cfg.WarmUpTime + user_cfg.CoolDownTime)

    all_exercises = load_data(db_conn, user_id=user_cfg.UserID, exercise_group=[str(collection_workout)])
    if not len(all_exercises):
        final_list = warm_up_exercise + post_workout_exercises
    else:
        # Main Exercises
        # TODO: this should be simplified (not doing all these on three seperate lines etc, maybe move the three into 1
        main_exercises = filter_main(all_exercises, specific_group=todays_workout, exercise_type=ExerciseType.MAIN)
        selected_main_exercise = copy.deepcopy(main_exercises.iloc[pick_exercise_idx(main_exercises, 1)])
        selected_main_exercise['WRR'] = training_type_main(selected_main_exercise.OneRepMax, wu=True)
        selected_main_exercise['TimeRequired'] = _count_time(selected_main_exercise['WRR'])
        selected_main_exercise_wu = copy.deepcopy(selected_main_exercise)
        selected_main_exercise_wu['ExerciseName'] = selected_main_exercise['ExerciseName'] + ' WU'
        selected_main_exercise_wu['WRR'] = selected_main_exercise['WRR'][:3]
        selected_main_exercise_wu['TimeRequired'] = _count_time(selected_main_exercise_wu['WRR'])
        selected_main_exercise_pr = copy.deepcopy(selected_main_exercise)
        selected_main_exercise_pr['WRR'] = selected_main_exercise['WRR'][3:]
        selected_main_exercise_pr['TimeRequired'] = _count_time(selected_main_exercise_pr['WRR'])
        selected_main_exercises = [selected_main_exercise_wu, selected_main_exercise_pr]
        # Secondary Exercises
        total_alloc_time -= selected_main_exercise['TimeRequired']
        secondary_exercises = filter_secondary(all_exercises, specific_group=todays_workout)
        selected_secondary_exercises = pick_secondary_exercises(secondary_exercises, total_alloc_time,
                                                                training_type_sec)
        # Putting it all together
        final_list = warm_up_exercise + selected_main_exercises + selected_secondary_exercises + post_workout_exercises
    return generate_table(day, final_list)


db_conn = setup_connection()

generate_workout('Sun', db_conn, load_user_config(db_conn, 'Gabor'))