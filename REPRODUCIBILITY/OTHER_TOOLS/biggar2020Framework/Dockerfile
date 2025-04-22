FROM ubuntu:24.04
RUN apt-get update -y
RUN apt-get upgrade -y

# Set the non-root user information
ARG VENUE=biggar2020Framework
ARG USER=biggar2020Framework
ARG UID=28338
ARG GID=28338

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
RUN sudo apt-get install unzip -y

RUN wget http://www.lrde.epita.fr/dload/spot/spot-2.13.tar.gz
RUN tar -xf /home/$USER/spot-2.13.tar.gz
WORKDIR /home/$USER/spot-2.13
RUN bash -c "/home/$USER/spot-2.13/configure --prefix /home/$USER/.local"
RUN sudo make
RUN sudo make install

RUN mkdir /home/$USER/python_venvs
RUN python3 -m venv /home/$USER/python_venvs/noname --system-site-packages
RUN /home/$USER/python_venvs/noname/bin/python3 -m pip install pyparsing


# Set the working directory
WORKDIR /home/$USER

COPY --chown=$UID:$GID lra-2970634-mm/ /home/$USER/
# COPY lra-2970634-mm.zip /home/$USER/
# RUN unzip lra-2970634-mm.zip


# for jupyterlab to work.
# EXPOSE 8888