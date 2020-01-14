from collections import namedtuple
from enum import Enum
import numpy
from datetime import datetime
from itertools import count

class ExerciseType(Enum):
    MAIN = 'main'
    SECONDARY = 'secondary'
    FILLER = 'x_filler'


class ExerciseGroup(Enum):
    SQUAT = 'squat'
    DEADLIFT = 'deadlift'
    CHEST = 'chest'
    SHOULDER = 'shoulder'
    BACK = 'back'
    HIIT = 'hiit'
    STRETCH = 'stretch'


# fields = ('ExerciseName', 'NumSets', 'NumReps', 'Weights', 'TimeRequired', 'RestTimer', 'ExerciseType',
#           'ExerciseGroup', 'Probability', 'LastUsed')
# defaults = (None, 0, 0, tuple(), 0, 0, None, None, 0, datetime.min)
# Exercise = namedtuple('Exercise', fields, defaults=defaults)
# fields_with_defaults = {field: default for field, default in zip(fields, defaults)}


class Exercise:
    _ids = count(0)

    def __init__(self,
                 ExerciseName=None,
                 NumSets=0,
                 NumReps=tuple(),
                 Weights=tuple(),
                 TimeRequired=0,
                 RestTimer=0,
                 ExerciseType=None,
                 ExerciseGroup=None,
                 Probability=0.0,
                 LastUsed=datetime.min):
        self.ExerciseName = ExerciseName
        self.NumSets = NumSets
        self.NumReps = NumReps
        self.Weights = Weights
        self.TimeRequired = TimeRequired
        self.RestTimer = RestTimer
        self.ExerciseType = ExerciseType
        self.ExerciseGroup = ExerciseGroup
        self.Probability = Probability
        self.LastUsed = LastUsed
        self.id = next(self._ids)

    def __repr__(self):
        return (
f'''
Exercise
ExerciseName:   {self.ExerciseName},
NumSets:        {self.NumSets},
NumReps:        {self.NumReps},
Weights:        {self.Weights},
TimeRequired:   {self.TimeRequired},
RestTimer:      {self.RestTimer},
ExerciseType:   {self.ExerciseType},
ExerciseGroup:  {self.ExerciseGroup},
Probability:    {self.Probability},
LastUsed:       {self.LastUsed}
'''
        )

ExerciseRotation = ('Push', 'Pull', 'Rest', 'Legs', 'Push', 'Pull', 'Legs')
WarmUpTime = 15
RollingTime = 10
StrechingTime = 10
TotalTime = 90
ExerciseDirectory = {
    'Legs':
        (
            # Main Exercises
            Exercise(ExerciseName='Squats',
                     NumSets=5,
                     NumReps=(8, 8, 8, 8, 5),
                     Weights=(20, 60, 100, 120, 140),
                     TimeRequired=25,
                     RestTimer=1,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.SQUAT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='deadlifts',
                     NumSets=5,
                     NumReps=(8, 8, 8, 8, 6),
                     Weights=(20, 60, 100, 120, 140),
                     TimeRequired=25,
                     RestTimer=1,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.DEADLIFT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            # Secondary Exercises
            Exercise(ExerciseName='Front Squats',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(50, 60, 70, 80),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SQUAT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Overhead Squats',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(40, 40, 40, 50),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SQUAT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Bulgarian Split Squats',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(20, 20, 20, 20),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SQUAT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Snatch',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(50, 60, 70, 80),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SQUAT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Power Cleans',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(40, 40, 40, 50),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SQUAT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Close Stand Squats',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(60, 60, 60, 60),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SQUAT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Leg Press',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8, 8),
                     Weights=(40, 80, 120, 160, 200),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SQUAT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Lunges',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(40, 40, 40, 40),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.DEADLIFT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Leg Curls',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(60, 70, 80, 100),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.DEADLIFT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Rack Pulls',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(60, 70, 80, 100),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.DEADLIFT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Good Mornings',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(60, 70, 80, 100),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.DEADLIFT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Hyperextensions',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(60, 70, 80, 100),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.DEADLIFT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            # Filler Exercises
            Exercise(ExerciseName='Seated Calv Raises',
                     NumSets=4,
                     NumReps=(24, 24, 24, 24),
                     Weights=(86, 95, 95, 95),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Standing Calv Raises',
                     NumSets=4,
                     NumReps=(24, 24, 24, 24),
                     Weights=(0, 0, 0, 0),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.5,
                     LastUsed=datetime.min),
        ),
    'Push':
        (
            # Chest Main Exercises
            Exercise(ExerciseName='Flat Barbell Bench Press',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 60, 80, 90, 100, 110),
                     TimeRequired=20,
                     RestTimer=1,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.4,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Flat Dumbbell Bench Press',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 26, 32, 36, 40, 42.5),
                     TimeRequired=20,
                     RestTimer=1,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.1,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Incline Barbell Bench Press',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 26, 32, 36, 40, 42.5),
                     TimeRequired=20,
                     RestTimer=1,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.1,
                     LastUsed=datetime.min),
            # Shoulder Main Exercises
            Exercise(ExerciseName='Military Barbell Press',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.4,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Military Dubbell Press',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Seated Dumbbell Press',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            # Chest Secondary Exercises
            Exercise(ExerciseName='Incline Dumbbell Bench Press',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Decline Barbell Bench Press',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Decline Dumbbell Bench Press',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Dumbbell Pull-Overs',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Cable Flies Mid',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Cable Flies High',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Cable Flies Low',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Dips',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='FlatDumbbell Flies',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Incline Dumbbell Flies',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Decline Dumbbell Flies',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.CHEST,
                     Probability=0.5,
                     LastUsed=datetime.min),
            # Shoulder Secondary Exercises
            Exercise(ExerciseName='Arnold Press',
                     NumSets=5,
                     NumReps=(8, 8, 8, 8, 8),
                     Weights=(18, 20, 22, 24, 28),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Front Dumbbell Raises',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(10, 10, 12, 12),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Lateral Dumbbell Raises',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Supermans',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(10, 10, 12, 12),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Around the World',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(10, 10, 12, 12),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Clean and Press',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(40, 40, 50, 50),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='One-Arm Cross Cable Laterals',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(10, 10, 12, 12),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='One-ArmSide Cable Laterals',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(10, 10, 12, 12),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Seated One-Arm Cross Cable Laterals',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(10, 10, 12, 12),
                     TimeRequired=20,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Standing Bent-Over Dumbbell Laterals',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(10, 10, 12, 12),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Upright Rows',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(42.5, 42.5, 42.5, 42.5),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.1,
                     LastUsed=datetime.min),
            # Shrugs
            Exercise(ExerciseName='Dumbbell Shrugs',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(42.5, 42.5, 42.5, 42.5),
                     TimeRequired=20,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.3,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Barbell Shrugs',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(80, 100, 120, 120),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.SHOULDER,
                     Probability=0.3,
                     LastUsed=datetime.min),
            # Triceps
            Exercise(ExerciseName='Close-Grip Bench Press',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(60, 60, 60, 60),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.3,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Cable Push-Downs Rope/Bar',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(36, 40, 40, 40),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.3,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Triceps Dip Machine',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(80, 100, 100, 100),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.3,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Cable Overhead-Press',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(42.5, 42.5, 42.5, 42.5),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.3,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Standing Dummbell Extension',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(8, 8, 8, 8),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.3,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Single-Arm Pull-Downs',
                     NumSets=4,
                     NumReps=(8, 8, 8, 8),
                     Weights=(5, 5, 5, 5),
                     TimeRequired=7,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.3,
                     LastUsed=datetime.min),
        ),

    'Pull':
        (
            # Main Back Exercises
            Exercise(ExerciseName='Wide Grip Pull Ups',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.BACK,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Bent over Rows',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=12,
                     RestTimer=1,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.BACK,
                     Probability=0.5,
                     LastUsed=datetime.min),
            # Secondary Back Exercises
            Exercise(ExerciseName='Standing T-Bar Rows',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.BACK,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Wide-Grip Seated Cable Rows',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.BACK,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Close-Grip Pull-Downs',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.BACK,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Single Arm Dumbbell Rows',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.BACK,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Close Grip Pull Ups',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.BACK,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Close-Grip Seated Rows',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.BACK,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Wide-Grip Cable Pull Downs',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=ExerciseGroup.BACK,
                     Probability=0.5,
                     LastUsed=datetime.min),
            # Biceps Exercises
            Exercise(ExerciseName='Barbell Curls',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Standing French Bar Curls',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Incline Dumbbel Normal Curls',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Incline Dumbbell Hammer Curls',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Roman Pad Curls',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=20,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Roman Pad Hammer Curls',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Standing Hammer Curls',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Seated Dumbbell Curls',
                     NumSets=6,
                     NumReps=(8, 8, 8, 8, 8, 8),
                     Weights=(20, 40, 50, 55, 60, 65),
                     TimeRequired=10,
                     RestTimer=1,
                     ExerciseType=ExerciseType.SECONDARY,
                     ExerciseGroup=None,
                     Probability=0.5,
                     LastUsed=datetime.min),
        ),
    'Warm Up':
        (
            Exercise(ExerciseName='Indoor Cycling',
                     NumSets=1,
                     NumReps=(1,),
                     Weights=(0,),
                     TimeRequired=15,
                     RestTimer=0,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.HIIT,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Rowing',
                     NumSets=1,
                     NumReps=(1,),
                     Weights=(0,),
                     TimeRequired=15,
                     RestTimer=0,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.HIIT,
                     Probability=0.5,
                     LastUsed=datetime.min),
        ),
    'Pre Streching':
        (
            Exercise(ExerciseName='Foam Rolling',
                     NumSets=1,
                     NumReps=(1,),
                     Weights=(0,),
                     TimeRequired=10,
                     RestTimer=0,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.STRETCH,
                     Probability=0.5,
                     LastUsed=datetime.min),
        ),
    'Post Streching':
        (
            Exercise(ExerciseName='Streching',
                     NumSets=1,
                     NumReps=(1,),
                     Weights=(0,),
                     TimeRequired=10,
                     RestTimer=0,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.STRETCH,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Massage Chair',
                     NumSets=1,
                     NumReps=(1,),
                     Weights=(0,),
                     TimeRequired=10,
                     RestTimer=0,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.STRETCH,
                     Probability=0.5,
                     LastUsed=datetime.min),
        ),
    'Rest':
        (
            Exercise(ExerciseName='Streching Whole Body',
                     NumSets=1,
                     NumReps=(1,),
                     Weights=(0,),
                     TimeRequired=15,
                     RestTimer=0,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.STRETCH,
                     Probability=0.5,
                     LastUsed=datetime.min),
            Exercise(ExerciseName='Massage Gun',
                     NumSets=1,
                     NumReps=(1,),
                     Weights=(0,),
                     TimeRequired=15,
                     RestTimer=0,
                     ExerciseType=ExerciseType.MAIN,
                     ExerciseGroup=ExerciseGroup.STRETCH,
                     Probability=0.5,
                     LastUsed=datetime.min),
        )
}
