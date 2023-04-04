#! /usr/bin/bash

help () { 
   echo "usage: docker-autograder-single.sh [options]"
   echo
   echo "Options:"
   echo "   -d <assignment-directory>"
   echo "   -c <code-file>"
   echo "   -t <timeout>"
   echo "   -e <show errors>"
   echo "   -i <docker-image>"
   echo "   -f <float-tolerance>"
}

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

while getopts "h?d:c:t:i:f:e" opt; do
    case "$opt" in
    h|\?)
        help
        exit 0
        ;;
    d)  
        working_dir=$OPTARG
        ;;
    c)  
        code_file=$OPTARG
        ;;
    i)  
        DOCKER_IMAGE=$OPTARG
        ;;
    t)  
        timeout=$OPTARG
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

echo $code_file
echo $working_dir

# create the docker container
echo "Creating container..."
docker create --name autograder --rm -it ${DOCKER_IMAGE} python /src/grade-single.py -d /assignment -c /deliverables/test.py -t ${timeout} -f ${float_tolerance} ${show_errors} 
# docker run --name autograder --rm -d ${DOCKER_IMAGE} bash

echo "Copying files..."
docker cp "${code_file}" autograder:/deliverables/test.py
docker cp "${working_dir}/." autograder:/assignment/

echo "Autograder Started!"
docker start -a -i autograder
