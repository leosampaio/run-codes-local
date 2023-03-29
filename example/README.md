# Example Usage of run-codes-local

For each assignment you should be given two things: the **specification PDF** and the **test cases**. Let us try solving and grading a simple assignment created for this example

-------------

## Step 01: Download the Necessary Files

- [Example Specification PDF](A0_spec.pdf)
- [Example Test Cases](test_cases.zip)

## Step 02: Read the specification carefully. 

The specification should be very clear about *inputs* and *outputs*, including formatting information. This will be essencial for automatic grading to work. 

In this special assignment, all we have to do is implement a python program that takes an image filename and one coordinate as input; outputs the pixel value at the specified coordinate.

## Step 03: Code your solution.

You can code your own solution of course, but for the sake of this example we have coded two solutions, [one correct](solution.py) and [one with a typo](solution_typo.py).

It is important to notice how input was read in these solutions:

```python
filename = input().rstrip()
coordinates  = (int(input().rstrip()), int(input().rstrip()))
```

Notice how the `input()` builtin function is called to get one line at a time from standard input (`stdin`). All inputs in assignments that use run-codes-local will get their inputs via `stdin`. We also make use of the `.rstrip()` method from strings to clean up trailing whitespace characters such as `\n` in unix-derived OSs and `\n\r` in Windows.

## Step 04: Test your code with run-codes-local.

With your solution and the test codes in hand, you can now use run-codes-local to auto-grade yourself. First get to know run-codes-local, run `python grade-single.py -h` to get a summary of the parameters:

```
usage: grade-single.py [-h] [-d WORKING_DIR] [-c CODE] [-t TIMEOUT] [-e] [-f FLOAT_TOLERANCE]

Make the same thing run.codes would do

options:
  -h, --help            show this help message and exit
  -d WORKING_DIR, --working-dir WORKING_DIR
  -c CODE, --code CODE  File with python code
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds
  -e, --show-errors     Show errors/warnings for each test case
  -f FLOAT_TOLERANCE, --float-tolerance FLOAT_TOLERANCE
                        If the answer is a single floating value, include a tolerance
```

The most important ones are the `-d` and `-c` params. They are used respectively to tell run-codes-local the *folder where the test cases are (working directory)* and where *your coded solution is*.

Now that we know how it works, let us run our own solution through it, starting with the one with a typo:

```
>> python grade-single.py -d example/ -c example/solution_typo.py

Running Case 01
Took 0.12s to run
There were errors/warnings when running!
    Expected answer: 117 71 47
    Computed Answer: 117 71 71
    Wrong, sorry
Running Case 02
Took 0.12s to run
There were errors/warnings when running!
    Expected answer: 90 72 62
    Computed Answer: 90 72 72
    Wrong, sorry
Running Case 03
Took 0.13s to run
There were errors/warnings when running!
    Expected answer: 235 229 217
    Computed Answer: 235 229 229
    Wrong, sorry
```

Seems like we got all of the test cases wrong because of our typo! Let us run the fixed version then:

```
>> python grade-single.py -d example/ -c example/solution.py

Running Case 01
Took 0.25s to run
There were errors/warnings when running!
    Expected answer: 117 71 47
    Computed Answer: 117 71 47
    It is Correct!
Running Case 02
Took 0.15s to run
There were errors/warnings when running!
    Expected answer: 90 72 62
    Computed Answer: 90 72 62
    It is Correct!
Running Case 03
Took 0.13s to run
There were errors/warnings when running!
    Expected answer: 235 229 217
    Computed Answer: 235 229 217
    It is Correct!
```

Now this is better, this solution is ready for submission! Or is it?? There is an improved and recommended way of running run-codes-local so that we can be sure it will work the same way in a Teaching Assistant computer.

## Running the tests on a Docker Container

Because all computers are different, we write a script to run your solution and do the grading under a common Docker container.

Docker containers are super lightweight virtual machines. That means we can guarantee solutions are graded under the same Operational System and with the same versions of packagers installed. We *strongly recommend* (please) you test your code under the container as well to avoid discrepancies when the grades come. It is super easy to do:

- Install [docker](https://docs.docker.com/get-docker/)
- Change the `python grade-single.py` command for `bash docker-autograder-single.sh`. The parameters are all the same.

And that is it! The container is removed after grading is finished and your code was graded under a common environment!
