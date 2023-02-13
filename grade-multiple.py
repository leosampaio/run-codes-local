import autograder

import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Make the same thing run.codes would do')
    parser.add_argument('-d', "--working-dir", default="./")
    parser.add_argument('-c', '--code-delivery-dir', type=str, default='./',
                        help="Directory with python codes inside")
    parser.add_argument('-m', "--metadata-csv", type=str,
                        help="CSV file with names and user IDs")
    parser.add_argument('--timeout', type=int,
                        help="Timeout in seconds")
    parser.add_argument('--use-case-as-params', action='store_true',
                        help="Set to use case input as params to script instead of using file redirection")

    args = parser.parse_args()

    grader = autograder.CodeAutoGrader(args.working_dir)

    students = autograder.find_all_student_codes(
        deliverables_dir=args.code_delivery_dir,
        metadata_csv_file=args.metadata_csv)

    autograder.grade_multiple_students(students, grader)

if __name__ == '__main__':
    main()
