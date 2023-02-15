# run-codes-local
## a simple substitute for the beloved run.codes, but it runs locally

-------------------
### Single Homework Usage (for students testing their codes)


To run locally on your machine:

```
grade-single.py [-h] [-d WORKING_DIR] [-c CODE] [-t TIMEOUT] [-e]
```
where `-d` sets the assignment directory, with case inputs and outpus plus other necessary files. `-c` sets your own python code. `-e` shows errors for each test case at the end. 

To run locally on you machine, but under the common docker container:

```
docker-autograder-single.sh [-h] [-d WORKING_DIR] [-c CODE] [-t TIMEOUT] [-e]
```
where the parameters are the same but you need to have docker installed. This is the preferred method to test since it yields the same results the Teaching Assistants will get when they run on their machines.

-----------
### Multiple Homeworks Usage (for Teaching Assistants grading multiple students)

To run locally on your machine:

```
grade-multiple.py [-h] [-d WORKING_DIR] [-c CODE_DELIVERY_DIR] [-o OUTPUT_CSV] [-m METADATA_CSV] [-t TIMEOUT]
```
where `-c` specifies the directory with multiple code files inside (one for each student). `-o` specifies the output csv with all results. `-m` specifies student names and IDs, and the python files in the code directory should match these IDs.

To run locally, but inder a common docker container (much prefeered for consistency):

```
docker-autograder-multiple.sh [-h] [-d WORKING_DIR] [-c CODE_DELIVERY_DIR] [-o OUTPUT_CSV] [-m METADATA_CSV] [-t TIMEOUT]
```