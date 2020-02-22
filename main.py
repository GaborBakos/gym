import subprocess
import pandas
import datetime
import fileinput

pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)
DayList = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')


if __name__ == '__main__':
    user_input = [90, 90, 90, 90, 90, 120, 120]
    current_week_num = datetime.date.today().isocalendar()[1]
    user_id = 'Gabor'
    collection_folder = "C:\\Users\\Gabor\\PycharmProjects\\gym\\weekly_exercises\\"
    configuring_call = (
        f"papermill gym_weekly_template.ipynb "
        f"gym_weekly_template_{user_id.lower()}.ipynb -p USER_ID {user_id}")
    process_call = (
        f"jupyter nbconvert gym_weekly_template_{user_id.lower()}.ipynb"
        f" --template nbextensions --to html --execute --output {collection_folder}week_{current_week_num}.html")
    remove_tmp_template = f"rm gym_weekly_template_{user_id}.ipynb"
    # Setting up the user_id
    subprocess.check_output(configuring_call)
    # Executing and rendering HTML
    subprocess.check_output(process_call)
    subprocess.check_output(remove_tmp_template)
    for line in fileinput.input(f"{collection_folder}week_{current_week_num}.html", inplace=True):
        if "gym_weekly_template" in line:
            line = line.replace("gym_weekly_template", f"Exercises for Week {current_week_num}")
        if "Exercises for Week __" in line:
            line = line.replace("__", str(current_week_num))
        if """<div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># Parameters</span>""" in line:
            line = ''
        if "USER_ID" in line:
            line = ''
        print(line, end='')


# TODO 1: Create notebook template for exercises (jupyter notebook notebook_name.ipynb)
# UPDATE 1: Something preliminary is there already
# TODO 2: Populate template with latest exercises (how to automate this?)
# UPDATE 2: The code is already there, just needs to render
# TODO 3: Render exercise notebook into HTML (jupyter nbconvert notebook_name.ipynb --to html --output output.html)
# TODO 4: Upload HTML to GitHub (not sure yet)
