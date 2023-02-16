import autograder

import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Make the same thing run.codes would do')
    parser.add_argument('-d', "--working-dir", default="./")
    parser.add_argument('-c', '--code-delivery-dir', type=str, default='./',
                        help="Directory with python codes inside")
    parser.add_argument('-o', '--output-csv', type=str,
                        help="File path for output csv")
    parser.add_argument('-m', "--metadata-csv", type=str,
                        help="CSV file with names and user IDs")
    parser.add_argument('-t', '--timeout', type=int,
                        help="Timeout in seconds")
    parser.add_argument('-f', '--float-tolerance', type=float, default=0.0,
                        help="If the answer is a single floating value, include a tolerance")

    args = parser.parse_args()

    grader = autograder.CodeAutoGrader(args.working_dir, timeout=args.timeout, float_tolerance=args.float_tolerance)

    students = autograder.find_all_student_codes(
        deliverables_dir=args.code_delivery_dir,
        metadata_csv_file=args.metadata_csv)

    evaluations = autograder.grade_multiple_students(students, grader)
    autograder.generate_csv_from_evaluated_students(evaluations, grader, args.output_csv)

if __name__ == '__main__':
    main()
