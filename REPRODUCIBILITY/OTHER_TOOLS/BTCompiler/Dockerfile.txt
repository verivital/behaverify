FROM ubuntu:24.04
RUN apt-get update -y
RUN apt-get upgrade -y

# Set the non-root user information
ARG VENUE=BTCompiler
ARG USER=BTCompiler
ARG UID=28334
ARG GID=28334

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
RUN sudo apt-get install build-essential -y
# #^GCC
RUN sudo apt-get install unzip bubblewrap -y
# needed for opam
RUN sudo apt-get install libgmp-dev pkg-config -y
# needed for ROCQ

RUN bash -c "printf '\n\n' | sh <(curl -fsSL https://opam.ocaml.org/install.sh)"
#^opam
RUN bash -c "eval $(opam env --switch=default)"
RUN opam init -y
RUN opam install xmlm -y
RUN opam pin add rocq-prover 9.0.0 -y
# install rocq
# RUN opam pin add rocq-prover $NEW_VERSION -y
# update rocq
#^ROCQ
RUN git clone https://github.com/CARVE-ROBMOSYS/BTCompiler

