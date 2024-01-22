FROM ubuntu:22.04
RUN apt-get update -y
RUN apt-get upgrade -y

# Set the non-root user information
ARG USER=user
ARG UID=1000
ARG GID=1000

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

RUN sudo apt-get install python3 pip git -y
ENV PIP_ROOT_USER_ACTION=ignore
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install py_trees textx onnxruntime
