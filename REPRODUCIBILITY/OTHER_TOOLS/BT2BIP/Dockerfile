FROM ubuntu:24.04
RUN apt-get update -y
RUN apt-get upgrade -y

# Set the non-root user information
ARG VENUE=BT2BIP
ARG USER=BT2BIP
ARG UID=28336
ARG GID=28336

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
RUN sudo apt-get install cmake build-essential -y

RUN git clone https://github.com/leethomason/tinyxml2.git
RUN mkdir /home/$USER/tinyxml2/build
WORKDIR /home/$USER/tinyxml2/build
RUN cmake ..
RUN make -j
RUN sudo make install -j


# Set the working directory
WORKDIR /home/$USER

RUN git clone https://github.com/789wpw/xml2bip.git
RUN mkdir /home/$USER/xml2bip/build
WORKDIR /home/$USER/xml2bip/build
RUN cmake ..
RUN make -j


# Set the working directory
WORKDIR /home/$USER
