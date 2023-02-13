import autograder

import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Make the same thing run.codes would do')
    parser.add_argument('-d', "--working-dir", default="./")
    parser.add_argument('-c', '--code', type=str, default='./main.py',
                        help="File with python code")
    parser.add_argument('--timeout', type=int,
                        help="Timeout in seconds")
    parser.add_argument('--use-case-as-params', action='store_true',
                        help="Set to use case input as params to script instead of using file redirection")

    args = parser.parse_args()

    grader = autograder.CodeAutoGrader(args.working_dir)
    grader.test_code_in_working_dir(args.code)

if __name__ == '__main__':
    main()
