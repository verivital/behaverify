FROM ubuntu:24.04
RUN apt-get update -y
RUN apt-get upgrade -y

# Set the non-root user information
ARG VENUE=ArcadeBT
ARG USER=ArcadeBT
ARG UID=28335
ARG GID=28335

# Create a non-root user
RUN groupadd -g $GID $USER \
    && useradd -u $UID -g $GID -m -s /bin/bash $USER

# Give sudo privileges to the non-root user
RUN apt-get update && apt-get install -y sudo \
    && echo "$USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USER \
    && chmod 0440 /etc/sudoers.d/$USER

# Set the working directory
WORKDIR /home/$USER

# Switch to the non-root user
USER $USER

RUN sudo apt-get install wget git curl -y
RUN sudo apt-get install python3 pip python3-venv -y
RUN sudo apt-get install cmake -y
RUN sudo apt-get install build-essential -y
RUN sudo apt-get install libgtest-dev libgoogle-glog-dev pkg-config -y

RUN wget -O /home/$USER/z3.tar.gz https://github.com/Z3Prover/z3/archive/refs/tags/z3-4.8.15.tar.gz
RUN tar -xf /home/$USER/z3.tar.gz --transform 's!^[^/]*!z3!'
RUN mkdir /home/$USER/z3/build

# Set the working directory
WORKDIR /home/$USER/z3/build
RUN cmake ../
RUN make

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/$USER/z3/build/
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu/


# Set the working directory
WORKDIR /home/$USER

RUN git clone https://github.com/embedded-software-laboratory/ArcadeBT

# Set the working directory
WORKDIR /home/$USER/ArcadeBT

RUN cmake -DZ3_DIR=../z3/build/ ./

# Set the working directory
WORKDIR /home/$USER