import autograder

import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Make the same thing run.codes would do')
    parser.add_argument('-d', "--working-dir", default="./")
    parser.add_argument('-c', '--code', type=str, default='./main.py',
                        help="File with python code")
    parser.add_argument('-t', '--timeout', type=int,
                        help="Timeout in seconds")
    parser.add_argument('-e', "--show-errors", action='store_true',
                        help="Show errors/warnings for each test case")

    args = parser.parse_args()

    grader = autograder.CodeAutoGrader(args.working_dir, timeout=args.timeout)
    evaluations = grader.test_code_in_working_dir(args.code)

    if args.show_errors:
        autograder.print_out_execution_errors(evaluations)

if __name__ == '__main__':
    main()
