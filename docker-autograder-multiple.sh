#! /usr/bin/bash

help () { 
   echo "usage: docker-autograder-single.sh [options]"
   echo
   echo "Options:"
   echo "   -d <assignment-directory>"
   echo "   -c <code-delivery-dir>"
   echo "   -o <output-csv>"
   echo "   -m <metadata-csv>"
   echo "   -t <timeout>"
   echo "   -e <show errors>"
   echo "   -i <docker-image>"
   echo "   -f <float-tolerance>"
}

# parser = argparse.ArgumentParser(
#         description='Make the same thing run.codes would do')
#     parser.add_argument('-d', "--working-dir", default="./")
#     parser.add_argument('-c', '--code-delivery-dir', type=str, default='./',
#                         help="Directory with python codes inside")
#     parser.add_argument('-o', '--output-csv', type=str,
#                         help="File path for output csv")
#     parser.add_argument('-m', "--metadata-csv", type=str,
#                         help="CSV file with names and user IDs")
#     parser.add_argument('--timeout', type=int,
#                         help="Timeout in seconds")

# default values
DOCKER_IMAGE=aleosampaio/image-processing:2023
show_errors=''
timeout=10
float_tolerance=0

# check for correct usage
if test $# -lt 2
then
    help
    exit 0
fi

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.

while getopts "h?d:c:t:i:o:m:e" opt; do
    case "$opt" in
    h|\?)
        help
        exit 0
        ;;
    d)  
        working_dir=$OPTARG
        ;;
    c)  
        code_files=$OPTARG
        ;;
    i)  
        DOCKER_IMAGE=$OPTARG
        ;;
    t)  
        timeout=$OPTARG
        ;;
    o)  
        out_csv=$OPTARG
        ;;
    m)  
        meta_csv=$OPTARG
        ;;
    f)  
        float_tolerance=$OPTARG
        ;;
    e)  
        show_errors='-e'
        ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
    esac
done

shift $((OPTIND-1))

[ "$1" = "--" ] && shift

# echo $code_files
# echo $working_dir
# echo ${timeout}

# create the docker container
echo "Creating container..."
docker create --name autograder -it ${DOCKER_IMAGE} python /src/grade-multiple.py -d /assignment -c /deliverables -t ${timeout} -f ${float_tolerance} -o out.csv -m /assignment/meta.csv ${show_errors} 

echo "Copying files..."
docker cp ${code_files}/. autograder:/deliverables/
docker cp ${working_dir}/. autograder:/assignment/
docker cp ${meta_csv} autograder:/assignment/meta.csv

echo "Autograder Started!"
docker start -a -i autograder

docker cp autograder:/src/out.csv $out_csv

docker rm autograder