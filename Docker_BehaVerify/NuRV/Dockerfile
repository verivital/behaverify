FROM ubuntu:23.10
RUN apt-get update -y \
    && apt-get upgrade -y

# Set the non-root user information
ARG USER=NuRV
ARG UID=56485
ARG GID=56485

# Create a non-root user
RUN groupadd -g $GID $USER \
    && useradd -u $UID -g $GID -m -s /bin/bash $USER

# Give sudo privileges to the non-root user
RUN apt-get update && apt-get install -y sudo \
    && echo "$USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USER \
    && chmod 0440 /etc/sudoers.d/$USER

RUN apt-get install libxml2 -y

# Set the working directory
WORKDIR /home/$USER

# Switch to the non-root user
USER $USER

WORKDIR /home/$USER
RUN mkdir /home/$USER/user_files