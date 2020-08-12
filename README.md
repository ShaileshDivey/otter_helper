# Autograding for Python/Jupyter/Excel using Otter Grader & GitHub Classroom or Blackboard

[![Custom badge](https://img.shields.io/endpoint?logo=slack&url=https%3A%2F%2Fraw.githubusercontent.com%2Fucbds-infra%2Fotter-grader%2Fmaster%2Fslack-shields.json)](https://join.slack.com/t/otter-grader/shared_invite/enQtOTM5MTQ0MzkwMTk0LTBiNWIzZTYxNDA2NDZmM2JkMzcwZjA4YWViNDM4ZTgyNDVhNDgwOTQ0NjNlZjcwNmY5YzJiZjZhZGNhNzc5MjA)

I've seen that quite a few other people teaching analytics have been discussing different autograding solutions.  This is my effort to create something that is relatively easy to use and can flexibly grade excel or python assignments.  

Generally, the workflow is as follows:

  (1) Use [GitHub Classroom](https://classroom.github.com) or Blackboard to collect assignments.  I can hear you already, I don't want to use git, it is too complicated.  It really is extremely easy, and it is a good learning experience for the students.  If you aren't a git users, you can easily [drag and drop a file to GitHub using the Web interface.](https://help.github.com/en/github/managing-files-in-a-repository/adding-a-file-to-a-repository)

  (2) Maintain all of the aspects of an assignment via a configuration file and roster.  This details aspects of the tests and the students.  If you collect notebooks via GitHub, this will allow a translation between GitHub and other notebooks.

  (3) Run the grading notebook.  The grading notebook will (a.) load the configuration files with information on the setup, (b.) copy the notebook file from the github repository to a /tmp folder for grading, (c.) append grading code to the bottom of the notebook.  (d.) execute the notebook. (d.) Output a JSON file with the results.

Give it a try with the attached notebook and grade the sample exercises.  

# Homework Grading
The goal of this is to develop a robust homework grading system which combines Google Colab + Jupyter Notebooks + GitHub Classroom + Otter Grader + Blackboard.



### Setup
The setup uses a based Andaconda Python installation.

```
pip install otter-grader
```

  1. If grading Python, Make sure that Docker is installed and the Docker Daemon is running.  You can download Docker [here](https://docs.docker.com/get-docker/).

  2. Clone the `Otter Helper` repository from [here](https://github.com/jkuruzovich/otter_helper).

  3.  Download assignment from Blackboard or GitHub and put it in the `assignments/<course>/<assignment>` directory. If you then paste your solution in this directory, it will be a good test that it was possible to get 100% on all of the tests.

  4. Update the `/config/course/<course>.yml` file with the appropriate configuration and assignments.

  5. Verify that the appropriate tests and data are in the associated `config/course/assignment/` folder.

  6. Verify that the appropriate files specified in the assignments are in the associated `config/course/files/` folder.

  7. Verify that the roster is setup in `config/course/roster.xlsx`. This includes 1 sheet which maps GitHub id to student id (if using GitHub classroom) and 1 that is a template downloaded from Blackboard.

  8. Update set the `course` and `assignment_id` varaibles in the `grade.ipynb` notebook to be consistent with the paths files downloaded and the `config.yml` file. To run the sample assignments, just keep `course` set to `sample-class` and select `blackboard` or `github-classroom` for the `assignment_id`.

**After completing the above, you are run the [grade-python.ipynb notebook](https://github.com/jkuruzovich/otter_helper/blob/master/notebooks/grade-python.ipynb) or [grade-excel.ipynb notebook](https://github.com/jkuruzovich/otter_helper/blob/master/notebooks/grade-python.ipynb).**  

Good luck! Please post any questions here or the Otter Slack channel.
