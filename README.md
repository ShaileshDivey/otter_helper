# Autograding for Python/Jupyter/Excel using Otter Grader & GitHub Classroom or Blackboard

[![Custom badge](https://img.shields.io/endpoint?logo=slack&url=https%3A%2F%2Fraw.githubusercontent.com%2Fucbds-infra%2Fotter-grader%2Fmaster%2Fslack-shields.json)](https://join.slack.com/t/otter-grader/shared_invite/enQtOTM5MTQ0MzkwMTk0LTBiNWIzZTYxNDA2NDZmM2JkMzcwZjA4YWViNDM4ZTgyNDVhNDgwOTQ0NjNlZjcwNmY5YzJiZjZhZGNhNzc5MjA)

I've seen that quite a few other people teaching analytics have been discussing different autograding solutions.  This is my effort to create something that is relatively easy to use and can flexibly grade Excel or Python assignments.  

You can watch a video walkthrough of the project here:

[![](http://img.youtube.com/vi/3PnOA6UMK9w/0.jpg)](http://www.youtube.com/watch?v=3PnOA6UMK9w "Video Overview of Project")

Generally, the workflow is as follows:

  (1) Use [GitHub Classroom](https://classroom.github.com) or Blackboard to collect assignments.  I can hear you already, I don't want to use git, it is too complicated.  It really is extremely easy, and it is a good learning experience for the students.  If you aren't a git users, you can easily [drag and drop a file to GitHub using the Web interface.](https://help.github.com/en/github/managing-files-in-a-repository/adding-a-file-to-a-repository)

  (2) Maintain all of the aspects of an assignment via a configuration file and roster.  This details aspects of the tests and the students.  If you collect notebooks via GitHub, this will allow a translation between GitHub and other notebooks.

  (3) Run the grading notebook for Python or Excel.  The grading notebook will (a.) load the configuration files with information on the setup, (b.) copy the notebook file from the github repository to a /tmp folder for grading, (c.) execute and grade the notebook (d.) Output the results in a format that can be uploaded to Blackboard.

Give it a try with the attached notebook and grade the sample exercises.  


### Installation
The setup uses a based Andaconda Python installation.

Clone the `Otter Helper` repository from [here](https://github.com/jkuruzovich/otter_helper).

*Docker*

I find it is best to customize your docker container and build it if grading locally. If you add your requirements for a single class docker container and not to each assignment, overall grading will go much faster. Make sure that Docker is installed and the Docker Daemon is running.  You can download Docker [here](https://docs.docker.com/get-docker/).

Uncomment the cells below and run it. Be sure to keep the ! as this is run via the command line.

Additional information on building the Docker image can be found here.

```
docker build . -t otter-helper:latest
```

*Otter Package Installation*

Use the command below to install Otter Grader.
```
pip install otter-grader
```

After installing you must be able to run the command `otter -help` from the command line.

### Grading
Once you have completed the installation, you are ready to start grading your assignment.  If you just want to see how it works just skip past these and go directly to the [grade-python.ipynb notebook](https://github.com/jkuruzovich/otter_helper/blob/master/notebooks/grade-python.ipynb) or [grade-excel.ipynb notebook](https://github.com/jkuruzovich/otter_helper/blob/master/notebooks/grade-python.ipynb).

  1.  Download assignment from Blackboard or GitHub and put it in the `assignments/<course>/<assignment>` directory. If you then paste your solution in this directory, it will be a good test that it was possible to get 100% on all of the tests.

  2. Update the `/config/course/<course>.yml` file with the appropriate configuration and assignments.

  3. Verify that the appropriate tests and data are in the associated `config/course/assignment/` folder.

  4. Verify that the appropriate files specified in the assignments are in the associated `config/course/files/` folder.

  5. Verify that the roster is setup in `config/course/roster.xlsx`. This includes 1 sheet which maps GitHub id to student id (if using GitHub classroom) and 1 that is a template downloaded from Blackboard.



**After completing the above, you are run the [grade-python.ipynb notebook](https://github.com/jkuruzovich/otter_helper/blob/master/notebooks/grade-python.ipynb) or [grade-excel.ipynb notebook](https://github.com/jkuruzovich/otter_helper/blob/master/notebooks/grade-python.ipynb).**  

Good luck! Please post any questions here or the Otter Slack channel.
