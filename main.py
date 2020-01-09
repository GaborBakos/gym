import numpy
import pandas
import copy
from datetime import datetime

from exercises import ExerciseDirectory, ExerciseRotation, ExerciseType, Exercise


pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
DayList = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')


flatten = lambda l: [item for sublist in l for item in sublist]


def remaining_time(time, exercises):
    if isinstance(exercises, Exercise):
        return time - exercises.TimeRequired
    else:
        for exercise in exercises:
            time -= exercise.TimeRequired
        return time


def pick_exercise_idx(exercise_list, num_choices):
    probability_distribution = numpy.array([exercise.Probability
                                            if exercise.Probability is not None
                                            else 0
                                            for exercise in exercise_list])
    probability_distribution /= probability_distribution.sum()
    return int(numpy.random.choice(range(len(exercise_list)), num_choices, p=probability_distribution))


def pick_secondary_exercises(exercise_list, allocated_time):
    res_secondaries = []
    res_fillers = []
    while allocated_time > 0 and len(exercise_list):
        exercise_idx = pick_exercise_idx(exercise_list, 1)
        if allocated_time - exercise_list[exercise_idx].TimeRequired < 0:
            del exercise_list[exercise_idx]
            continue
        if exercise_list[exercise_idx].ExerciseGroup is not None:
            res_secondaries.append(exercise_list[exercise_idx])
            del exercise_list[exercise_idx]
            allocated_time -= res_secondaries[-1].TimeRequired
        else:
            res_fillers.append(exercise_list[exercise_idx])
            del exercise_list[exercise_idx]
            allocated_time -= res_fillers[-1].TimeRequired
    return res_secondaries + res_fillers


def subset_exercise_list(exercise_list, exercise_type=ExerciseType.MAIN, exercise_group=None):
    ex = copy.deepcopy(exercise_list)
    if exercise_group is not None:
        ex = list(filter(lambda x: x if x.ExerciseGroup == exercise_group or x.ExerciseGroup is None else None, ex))
    return list(filter(lambda x: x if x.ExerciseType == exercise_type else None, ex))


def find_workout_for_day(day):
    return ExerciseRotation[DayList.index(day) % len(ExerciseRotation)]


# fields = ('ExerciseName', 'NumSets', 'NumReps', 'Weights', 'TimeRequired', 'RestTimer', 'ExerciseType',
#           'ExerciseGroup', 'Probability', 'LastUsed')

def generate_table(day, exercise_list, timed_workout=True):
    index = []
    max_sets = -numpy.inf
    for exercise in exercise_list:
        index.append(exercise.ExerciseName)
        max_sets = max(max_sets, exercise.NumSets)
    index = pandas.Index(index, name='Exercises')
    columns = pandas.Index(['Weight', 'Reps'] * max_sets, name=day)
    timer_columns = pandas.Index(['Time Alloc', 'Rest'])
    data = numpy.empty((len(exercise_list), max_sets * 2))
    timings = numpy.empty((len(exercise_list), 2), dtype=int)
    for idx, el in enumerate(exercise_list):
        row = flatten([[weight, rep] for weight, rep in zip(el.Weights, el.NumReps)])
        times = [el.TimeRequired, el.RestTimer]
        while len(row) < max_sets * 2:
            row.extend([None, None])
        data[idx, :] = row
        timings[idx, :] = times
    timer_df = pandas.DataFrame(timings, index, timer_columns)
    df = pandas.DataFrame(data, index, columns)
    if timed_workout:
        return pandas.concat([df, timer_df], axis=1)
    return df


def generate_workout(day, total_allocated_time):
    warm_up_exercise = (ExerciseDirectory['Warm Up'][1]
                        if find_workout_for_day(day) == 'Pull'
                        else ExerciseDirectory['Warm Up'][0])
    total_allocated_time = remaining_time(total_allocated_time, warm_up_exercise)
    post_workout_routine = list(ExerciseDirectory['Post Streching'])
    total_allocated_time = remaining_time(total_allocated_time, post_workout_routine)
    all_exercises = ExerciseDirectory[find_workout_for_day(day)]
    main_exercises = subset_exercise_list(all_exercises, exercise_type=ExerciseType.MAIN)
    selected_main_exercise = main_exercises[pick_exercise_idx(main_exercises, 1)]
    total_allocated_time = remaining_time(total_allocated_time, selected_main_exercise)
    # total_allocated_time -= selected_main_exercise.TimeRequired
    secondary_exercises = (subset_exercise_list(all_exercises,
                                                exercise_type=ExerciseType.SECONDARY,
                                                exercise_group=selected_main_exercise.ExerciseGroup))
    selected_secondary_exercises = pick_secondary_exercises(secondary_exercises, total_allocated_time)
    final_list = [warm_up_exercise] + [selected_main_exercise] + selected_secondary_exercises + post_workout_routine

    return generate_table(day, final_list)

if __name__ == '__main__':
    total_workout_time = input("Please enter how many minutes you have for your gym session:\n ")
    print(generate_workout(DayList[datetime.today().weekday()], total_workout_time))


