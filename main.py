import subprocess
import pandas
import datetime
import fileinput

from formatter import column_formater, table_formatter, format_df
from exercise_generator import generate_workout

pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
DayList = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')


def generate_weekly_schedule(workout_times_list, cwn):
    for idx, total_time in enumerate(workout_times_list):
        df = generate_workout(DayList[idx], total_time)
        with open(f"C:\\Users\\Gabor\\PycharmProjects\\gym\\week_{cwn}.html", "r+") as f:
            f.write(
                format_df(df, column_style=column_formater, table_style=table_formatter).render().replace("nan", "") +
                '\n\n\n\n\n')
        # with open(f"C:\\Users\\Gabor\\PycharmProjects\\gym\\week_{cwn}.html", "r+") as f:
        #     f.write(
        #         format_df(df, column_style=column_formater, table_style=table_formatter).render().replace("nan", "") +
        #         '\n\n\n\n\n')
        #     print(df)


if __name__ == '__main__':
    user_input = [90, 90, 90, 90, 90, 120, 120]
    # for current_week_num in range(10):
    current_week_num = datetime.date.today().isocalendar()[1]
    collection_folder = "C:\\Users\\Gabor\\PycharmProjects\\gym\\weekly_exercises\\"
    subprocess.call(
            f"jupyter nbconvert gym_weekly_template.ipynb"
            f" --template nbextensions --to html --execute --output {collection_folder}week_{current_week_num}.html")
    # with open(f"{collection_folder}week_{current_week_num}.html", "r") as f:
    #     for line in f:
    #         line.replace("gym_weekly_template", f"Exercises for Week {current_week_num}")

    for line in fileinput.input(f"{collection_folder}week_{current_week_num}.html", inplace=True):
        if "gym_weekly_template" in line:
            line = line.replace("gym_weekly_template", f"Exercises for Week {current_week_num}")
        if "Exercises for Week __" in line:
            line = line.replace("__", str(current_week_num))
        print(line, end='')
        # generate_weekly_schedule(user_input, current_week_num)


# TODO 1: Create notebook template for exercises (jupyter notebook notebook_name.ipynb)
# UPDATE 1: Something preliminary is there already
# TODO 2: Populate template with latest exercises (how to automate this?)
# UPDATE 2: The code is already there, just needs to render
# TODO 3: Render exercise notebook into HTML (jupyter nbconvert notebook_name.ipynb --to html --output output.html)
# TODO 4: Upload HTML to GitHub (not sure yet)
