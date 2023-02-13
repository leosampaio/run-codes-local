import glob
import os
import collections
import re
import shutil
import subprocess
import time
import io
import csv


CaseFile = collections.namedtuple("CaseFile", ["case_id", "in_file", "out_file", "in_content", "out_content"])
Evaluation = collections.namedtuple("Evaluation", ["case", "time", "answer", "is_correct", "errors"])
StudentDeliverable = collections.namedtuple("StudentDeliverable", ["name", "identifier", "code_file"])
EvaluatedStudent = collections.namedtuple("EvaluatedStudent", ["student", "evaluation"])


def find_all_case_files(working_dir):
    case_files = []
    input_files = glob.glob(os.path.join(working_dir, "case*.in"))
    for input_file in input_files:
        case_id = re.findall(r".*case(\d+).in", input_file)[0]
        output_file = os.path.join(working_dir, f"case{case_id}.out")
        if os.path.exists(output_file):
            with open(input_file, mode='r') as testcase:
                in_content = testcase.readlines()
                in_content = ''.join(in_content)
            with open(output_file, mode='r') as correcttest:
                out_content = correcttest.readlines()
                out_content[-1] = out_content[-1].rstrip()
                out_content = ''.join(out_content)
            case_file = CaseFile(case_id=case_id, in_file=input_file, out_file=output_file,
                                 in_content=in_content, out_content=out_content)
            case_files.append(case_file)
        else:
            raise KeyError(f"File {input_file} does not have correspondent file case{case_id}.in")

    # sort the cases
    case_files = sorted(case_files, key=lambda x: x.case_id)

    return case_files


def find_all_student_codes(deliverables_dir, metadata_csv_file, name_key="Nome Completo", id_key="Número USP"):
    student_to_file = {}
    py_files = glob.glob(os.path.join(deliverables_dir, "*/*.py"))
    for py_file in py_files:
        student_id = re.findall(r'[0-9]+', os.path.basename(py_file))[0]
        student_to_file[student_id] = py_file

    students = []
    with open(metadata_csv_file, mode='r') as csv_file:
        metadata_csv_reader = csv.DictReader(csv_file)
        for metadata_row in metadata_csv_reader:
            name = metadata_row[name_key]
            identifier = metadata_row[id_key]
            try:
                student_code = student_to_file[identifier]
                student = StudentDeliverable(name=name, identifier=identifier, code_file=student_code)
            except KeyError:
                print(f"Student {name}, id {identifier}, did not deliver homework")
                student = StudentDeliverable(name=name, identifier=identifier, code_file=None)
            
            students.append(student)

    students = sorted(students, key=lambda x: x.name)
    return students

def grade_multiple_students(students, grader):
    evaluated_students = []
    for student in students:
        if student.code_file is not None:
            print(f"Grading student {student.name}, id {student.identifier}")
            student_eval = grader.test_code_in_working_dir(student.code_file)
        else:
            student_eval = None
        evaluated_student = EvaluatedStudent(student=student, evaluation=student_eval)
        evaluated_students.append(evaluated_student)
    return evaluated_students

class CodeAutoGrader(object):

    def __init__(self, working_dir, use_cases_as_file=True, timeout=10):
        self.working_dir = working_dir
        self.case_files = find_all_case_files(working_dir)
        self.use_cases_as_file = use_cases_as_file
        self.timeout = timeout

    def test_code_in_working_dir(self, code_file, verbose=True):

        if code_file[-3:] != ".py":
            raise ValueError(f"Code file {code_file} not currently supported by run-codes-local")

        # copy code to working directory
        shutil.copyfile(code_file, os.path.join(self.working_dir, "./autograder_test.py"))

        complete_eval = []
        for case in self.case_files:

            time_to_run, answer, errors = self.run_case(case)
            is_correct = self.check_case(case, answer, verbose=verbose)

            evaluation = Evaluation(case=case, time=time_to_run, answer=answer,
                                    is_correct=is_correct, errors=errors)
            complete_eval.append(evaluation)

        return complete_eval

    def run_case(self, case):
        rightnow = time.perf_counter()
        try:
            result = subprocess.run(["python", "./autograder_test.py"],
                                    input=case.in_content.encode(), capture_output=True, timeout=self.timeout, cwd=self.working_dir)
        except subprocess.TimeoutExpired as e:
            totaltime = (time.perf_counter() - rightnow)
            return totaltime, None, "Timeout"
        totaltime = (time.perf_counter() - rightnow)

        answer = result.stdout.decode('utf-8').rstrip()
        errors = result.stderr.decode('utf-8').rstrip()

        return totaltime, answer, errors

    def check_case(self, case, answer, verbose=True):
        is_correct = answer == case.out_content
        if is_correct and verbose:
            print(f"Case {case.case_id}: {answer}, Right")
        elif verbose:
            print(f"Case {case.case_id}: {answer}, Wrong")

        return is_correct
