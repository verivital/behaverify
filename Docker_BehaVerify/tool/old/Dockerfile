FROM ubuntu:23.10
RUN apt-get update -y \
    && apt-get upgrade -y

# Set the non-root user information
ARG USER=behaverify
ARG UID=16227
ARG GID=16227

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

RUN sudo apt-get install git -y
RUN sudo apt-get install python3 pip python3-venv -y