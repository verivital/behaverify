FROM ubuntu:23.10
RUN apt-get update -y \
    && apt-get upgrade -y

# Set the non-root user information
ARG USER=LTL2BA
ARG UID=21404
ARG GID=21404

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

RUN sudo apt-get install g++ cmake make git autoconf libconfig-dev libtool -y

ADD https://api.github.com/repos/utwente-fmt/ltl2ba/git/refs/heads/master version.json
RUN git clone https://github.com/utwente-fmt/ltl2ba

# RUN mkdir /home/$USER/ltl2ba/build
# WORKDIR /home/$USER/ltl2ba/build
# RUN cmake ../
# RUN ../configure
# RUN make

WORKDIR /home/$USER/ltl2ba
RUN autoupdate
RUN autoreconf --install --force
# RUN autoconf -i -f
RUN ./configure
RUN make

WORKDIR /home/$USER