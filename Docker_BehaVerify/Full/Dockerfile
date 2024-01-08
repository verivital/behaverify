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



RUN sudo apt-get install python3 -y
RUN sudo apt-get install pip -y
ENV PIP_ROOT_USER_ACTION=ignore
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install py_trees
RUN python3 -m pip install textx
RUN sudo apt-get install git -y

RUN sudo apt-get install build-essential curl libffi-dev libffi8ubuntu1 libgmp-dev libgmp10 libncurses-dev libncurses5 libtinfo5 -y

RUN sudo apt-get install libgmp3-dev -y


# Install ghcup
ENV BOOTSTRAP_HASKELL_NONINTERACTIVE=1
RUN bash -c "curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh"
RUN bash -c "curl -sSL https://get.haskellstack.org/ | sh"

# Add ghcup to PATH
ENV PATH=${PATH}:/root/.local/bin
ENV PATH=${PATH}:/root/.ghcup/bin

# Install cabal
RUN bash -c "ghcup upgrade"
RUN bash -c "ghcup install cabal 3.6.2.0"
RUN bash -c "ghcup set cabal 3.6.2.0"

# Install GHC
RUN bash -c "ghcup install ghc 9.2.8"
RUN bash -c "ghcup set ghc 9.2.8"

# Update Path to include Cabal and GHC exports
RUN bash -c "echo PATH="$HOME/.local/bin:$PATH" >> $HOME/.bashrc"
RUN bash -c "echo export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH" >> $HOME/.bashrc"
RUN bash -c "source $HOME/.bashrc"


RUN mkdir behaverify && cd behaverify && git init && \
    git remote add -f origin https://github.com/verivital/behaverify && \
    echo "src/" >> .git/info/sparse-checkout && \
    echo "metamodel/" >> .git/info/sparse-checkout && \
    echo "Docker_BehaVerify/" >> .git/info/sparse-checkout && \
    git pull origin main
RUN chmod -R +x /home/user/behaverify/Docker_BehaVerify/*.sh
