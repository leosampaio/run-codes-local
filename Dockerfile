FROM opencvcourses/opencv:440

ENV DEBIAN_FRONTEND noninteractive

RUN mkdir -p /deliverables
RUN mkdir -p /assignment

# change workdir and add some files
WORKDIR /src
ADD ./requirements.txt ./

# install our beloved requirements
RUN pip install -U pip
RUN pip install -r requirements.txt

ADD ./autograder.py ./
ADD ./grade-multiple.py ./
ADD ./grade-single.py ./