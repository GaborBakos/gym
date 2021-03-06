from collections import namedtuple
from enum import Enum
import numpy
from datetime import datetime
from itertools import count


class ExerciseType(Enum):
    MAIN = 'main'
    SECONDARY = 'secondary'
    FILLER = 'x_filler'

    def __repr__(self):
        return f"{self}"


class ExerciseGroup(Enum):
    # Exercise Group
    LEGS = 'legs'
    PUSH = 'push'
    PULL = 'pull'
    # Specific Group
    SQUAT = 'squat'
    DEADLIFT = 'deadlift'
    CHEST = 'chest'
    SHOULDER = 'shoulder'
    BACK = 'back'
    # Other
    HIIT = 'hiit'
    STRETCH = 'stretch'
    REST = 'rest'

    def __repr__(self):
        return f"{self}"


class WorkoutType(Enum):
    STRENGTH = 'strength'
    MUSCLE = 'muscle'
    ENDURANCE = 'endurance'

    def __repr__(self):
        return f"{self}"


class Exercise:
    _ids = count(0)

    def __init__(self,
                 exercise_name=None,
                 exercise_type=None,
                 exercise_group=None,
                 specific_group=None,
                 probability=0.0):

        self.ExerciseName = exercise_name
        self.ExerciseType = exercise_type
        self.ExerciseGroup = exercise_group
        self.SpecificGroup = specific_group
        self.Probability = probability
        self.ID = next(self._ids)

    def __repr__(self):
        return (
f'''
Exercise
ID:             {self.ID},
ExerciseName:   {self.ExerciseName},
ExerciseType:   {self.ExerciseType},
ExerciseGroup:  {self.ExerciseGroup},
SpecificGroup:  {self.SpecificGroup},
Probability:    {self.Probability},
'''
        )


ExerciseRotation = (
    ExerciseGroup.CHEST,
    ExerciseGroup.BACK,
    ExerciseGroup.REST,
    ExerciseGroup.DEADLIFT,
    ExerciseGroup.SHOULDER,
    ExerciseGroup.BACK,
    ExerciseGroup.SQUAT)

CollectionExerciseStr = {
    'ExerciseGroup.CHEST': 'ExerciseGroup.PUSH',
    'ExerciseGroup.BACK': 'ExerciseGroup.PULL',
    'ExerciseGroup.REST': 'ExerciseGroup.REST',
    'ExerciseGroup.DEADLIFT': 'ExerciseGroup.LEGS',
    'ExerciseGroup.SHOULDER': 'ExerciseGroup.PUSH',
    'ExerciseGroup.SQUAT': 'ExerciseGroup.LEGS',
    }
CollectionExercise = {
    ExerciseGroup.CHEST: ExerciseGroup.PUSH,
    ExerciseGroup.BACK: ExerciseGroup.PULL,
    ExerciseGroup.REST: ExerciseGroup.REST,
    ExerciseGroup.DEADLIFT: ExerciseGroup.LEGS,
    ExerciseGroup.SHOULDER: ExerciseGroup.PUSH,
    ExerciseGroup.SQUAT: ExerciseGroup.LEGS,
    }

WarmUpTime = 15
RollingTime = 10
StrechingTime = 10
TotalTime = 90

ExerciseDirectory = {
    'Squat':
        (
            # Main Exercises
            Exercise(exercise_name='Barbell Squats',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.SQUAT,
                     probability=0.5),
            # Secondary Exercises
            Exercise(exercise_name='Front Squats',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.SQUAT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Overhead Squats',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.SQUAT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Bulgarian Split Squats',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.SQUAT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Snatch',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.SQUAT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Power Cleans',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.SQUAT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Close Stand Squats',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.SQUAT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Leg Press',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.SQUAT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Seated Calv Raises',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Standing Calv Raises',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     probability=0.5,
                     ),
        ),
    'Deadlift':
        (
            Exercise(exercise_name='Deadlifts',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.DEADLIFT,
                     probability=0.5,
                     ),
            # Secondary Exercises
            Exercise(exercise_name='Lunges',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.DEADLIFT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Leg Curls',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.DEADLIFT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Rack Pulls',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.DEADLIFT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Good Mornings',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.DEADLIFT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Hyperextensions',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.LEGS,
                     specific_group=ExerciseGroup.DEADLIFT,
                     probability=0.5,
                     ),
        ),
    'Chest':
        (
            # Chest Main Exercises
            Exercise(exercise_name='Flat Barbell Bench Press',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.4,
                     ),
            Exercise(exercise_name='Flat Dumbbell Bench Press',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.1,
                     ),
            Exercise(exercise_name='Incline Barbell Bench Press',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.1,
                     ),

            # Chest Secondary Exercises
            Exercise(exercise_name='Incline Dumbbell Bench Press',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Decline Barbell Bench Press',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Decline Dumbbell Bench Press',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Dumbbell Pull Overs',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Cable Flies Mid',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Cable Flies High',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Cable Flies Low',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Dips',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Flat Dumbbell Flies',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Inclide Dumbbell Flies',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Decline Dumbbell Flies',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.CHEST,
                     probability=0.5,
                     ),
        ),

    'Shoulder':
        (
            # Shoulder Main Exercises
            Exercise(exercise_name='Military Barbell Press',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.4,
                     ),
            Exercise(exercise_name='Military Dumbbell Press',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            Exercise(exercise_name='Seated Dumbbell Press',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            # Shoulder Secondary Exercises
            Exercise(exercise_name='Arnold Press',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Front Dumbbell Raises',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            Exercise(exercise_name='Lateral Dumbbell Raises',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            Exercise(exercise_name='Supermans',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            Exercise(exercise_name='Around the World',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            Exercise(exercise_name='Clean and Press',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            Exercise(exercise_name='One-Arm Cross Cable Laterals',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            Exercise(exercise_name='One-Arm Side Cable Laterals',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            Exercise(exercise_name='Seated One-Arm Cross Cable Laterals',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            Exercise(exercise_name='Standing Bent Over Dumbbell Laterals',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            Exercise(exercise_name='Upright Rows',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     specific_group=ExerciseGroup.SHOULDER,
                     probability=0.1,
                     ),
            # Shrugs

        ),
    'Triceps':
        (
            # Triceps
            Exercise(exercise_name='Close-Grip Bench Press',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     probability=0.3,
                     ),
            Exercise(exercise_name='Cable Push-Downs Rope/Bar',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     probability=0.3,
                     ),
            Exercise(exercise_name='Triceps Dip Machine',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     probability=0.3,
                     ),
            Exercise(exercise_name='Cable Overhead-Press',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     probability=0.3,
                     ),
            Exercise(exercise_name='Standing Dumbbell Extension',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     probability=0.3,
                     ),
            Exercise(exercise_name='Single-Arm Pull-Downs',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PUSH,
                     probability=0.3,
                     ),
        ),
    'Shrugs':
        (
            Exercise(exercise_name='Dumbbell Shrugs',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     probability=0.3,
                     ),
            Exercise(exercise_name='Barbell Shrugs',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     probability=0.3,
                     ),
        ),

    'Back':
        (
            # Main Exercises
            Exercise(exercise_name='Wide Grip Pull Ups',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.PULL,
                     specific_group=ExerciseGroup.BACK,
                     probability=0.5),
            Exercise(exercise_name='Bent over Rows',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.PULL,
                     specific_group=ExerciseGroup.BACK,
                     probability=0.5,
                     ),
            # Secondary Exercises
            Exercise(exercise_name='Standing T-Bar Rows',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     specific_group=ExerciseGroup.BACK,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Wide-Grip Seated Cable Rows',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     specific_group=ExerciseGroup.BACK,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Close-Grip Pull-Downs',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     specific_group=ExerciseGroup.BACK,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Single Arm Dumbbell Rows',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     specific_group=ExerciseGroup.BACK,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Close Grip Pull Ups',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     specific_group=ExerciseGroup.BACK,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Close-Grip Seated Rows',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     specific_group=ExerciseGroup.BACK,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Wide-Grip Cable Pull Downs',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     specific_group=ExerciseGroup.BACK,
                     probability=0.5,
                     ),
        ),
    'Biceps':
        (
            # Biceps Exercises
            Exercise(exercise_name='Barbell Curls',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Standing French Bar Curls',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Incline Dumbbel Normal Curls',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Incline Dumbbell Hammer Curls',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Roman Pad Curls',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Roman Pad Hammer Curls',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Standing Hammer Curls',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Seated Dumbbell Curls',
                     exercise_type=ExerciseType.SECONDARY,
                     exercise_group=ExerciseGroup.PULL,
                     probability=0.5,
                     ),
        ),
    'Warm Up':
        (
            Exercise(exercise_name='Stair Master',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.HIIT,
                     specific_group=ExerciseGroup.LEGS,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Indoor Cycling',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.HIIT,
                     specific_group=ExerciseGroup.PUSH,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Rowing',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.HIIT,
                     specific_group=ExerciseGroup.PULL,
                     probability=0.5,
                     ),
        ),
    'Pre Streching':
        (
            Exercise(exercise_name='Foam Rolling',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.STRETCH,
                     probability=0.5,
                     ),
        ),
    'Post Streching':
        (
            Exercise(exercise_name='Streching',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.STRETCH,
                     specific_group=ExerciseGroup.SQUAT,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Massage Chair',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.STRETCH,
                     probability=0.5,
                     ),
        ),
    'Rest':
        (
            Exercise(exercise_name='Streching Whole Body',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.STRETCH,
                     probability=0.5,
                     ),
            Exercise(exercise_name='Massage Gun',
                     exercise_type=ExerciseType.MAIN,
                     exercise_group=ExerciseGroup.STRETCH,
                     probability=0.5,
                     ),
        )
}
