CSCI Tool
=========

CSCI tool is a cli to create student GitHub repos, add assignment starter code,
collect submissions and grading those submissions.

Architecture
------------
`csci` was designed to be generic to be able to support different courses or
different assignments. Each assignment has two supporting python files,
`mutate.py` and `grade.py`. This lets `csci` provide useful functionality for a
wide range of assignment needs.  
All data that the `csci` tool needs resides in the organizations `meta` repo.
This meta repo stores a list of students (students.txt) as well as all student
submissions, and grader-student assignments for each assignment.

Instructions
------------

Installation  
`python3 setup.py install`
`csci_tool` requires Python3 and setuptools to install  
(on ubuntu `sudo apt install python3 && pip3 install setuptools`)


Usage  
First login - necessary before you can do anything useful  
`csci login`

Create repos for students:  
`csci create-repos students.txt` where students.txt is a text file where each
line is a student's information like so: `smagro@usc.edu vmagro` (email and
github username). If no file is specified, the tool will read from stdin.  
This will create a repo for each student like `hw_smagro`, add the student to
it's contributors and add the CP team as contributors.

Run a given mutator on all student repos:  
`csci mutate <mutation>` eg `csci mutate datalab`  

Collect code for all students:  
`csci collect <assignment name>` eg `csci collect datalab`

Run auto grading scripts for all student submissions:  
`csci grade --auto <assignment name>` eg `csci grade --auto datalab`

Assign students to graders randomly for human grading:  
`csci grader-assign <assignment name>` eg `csci grade datalab`

Manual grading convenience for assigned students to grade:  
`csci grade <assignment name>` eg `csci grade datalab`

Most commands above also take an optional positional argument `students` at the
end of the command that is a file to read the list of students instead of
`meta/students.txt`

Mutations
---------
`mutate.py` has the "mutation" code for the student repo. Mutations are how
code is added to a student repo. A mutation can be as simple as copying source
code files into another directory or as complicated as modifying existing code
or compiling a different version of project code for every student.

```python3
def mutate(student, source_dir):
    """Mutate student repo
    Current working dir is set to student repo working copy.
    Arguments:
      student (Student): properties: email, unix_name, github
      source_dir (PathLike): path to directory containing mutate.py
    """
```
`csci mutate` will run the specified `mutate` function and commit the changes
automatically.

Collection and Grading
----------------------
`csci collect <assignment name` will pull the current commit from each student
repository and add it as a submodule of the `meta` repo under
`submissions/<assignment name>/<student repo name>`
Additionally, it will comment on that commit on GitHub to notify the student
that the commit was collected for the assignment.

`csci grade --auto <assignment name>` runs the auto-grading script on each
student repo under `meta/submissions/<assignment name>` and writes the results
to `meta/submissions/grades_<assignment name>.csv`

`csci grade <assignment name>` is a convenience script for human grading that
will show files of interest for each student to the grader and prompt them for
a score. Each assignment defines files that should be looked at by the human
grader, `csci` will show the grader those files with a `less`-like interface,
and then prompt for a score when the grader is done viewing. The human grading
scripts write to the same file as the auto-grader, adding two columns to each
line, the human core and a comments text field.  
The human grading script also can be passed a text file of students to grade,
but by default looks in a file `meta/submissions/grade_<usc unix name>.txt`
