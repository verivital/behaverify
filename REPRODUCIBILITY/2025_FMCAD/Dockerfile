FROM ubuntu:22.04
RUN apt-get update -y
RUN apt-get upgrade -y

# Set the non-root user information
ARG VENUE=2025_FMCAD
ARG USER=BehaVerify_$VENUE
ARG UID=22238
ARG GID=22238

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

RUN sudo apt-get install wget git python3 pip python3-venv -y
RUN sudo apt-get install graphviz -y

ADD https://api.github.com/repos/verivital/behaverify/git/refs/heads/main version.json
# this makes sure we grab the newest version of the repo instead of reusing an older one

RUN git clone --filter=blob:none --no-checkout --depth 1 --sparse https://github.com/verivital/behaverify
WORKDIR /home/$USER/behaverify
RUN git sparse-checkout set --no-cone
RUN echo !/* > /home/$USER/behaverify/.git/info/sparse-checkout
RUN echo /REPRODUCIBILITY/$VENUE >> /home/$USER/behaverify/.git/info/sparse-checkout
RUN git checkout

RUN echo $USER > /home/$USER/user.txt
# this hopefully makes sure that we don't get weird conflicts between images depending on each other.

RUN python3 -m venv /home/$USER/python_venvs/behaverify
RUN /home/$USER/python_venvs/behaverify/bin/python3 -m pip install --upgrade pip
RUN /home/$USER/python_venvs/behaverify/bin/python3 -m pip install -r /home/$USER/behaverify/REPRODUCIBILITY/$VENUE/requirements/core.txt
RUN python3 -m venv /home/$USER/python_venvs/results
RUN /home/$USER/python_venvs/results/bin/python3 -m pip install --upgrade pip
RUN /home/$USER/python_venvs/results/bin/python3 -m pip install -r /home/$USER/behaverify/REPRODUCIBILITY/$VENUE/requirements/drawing.txt

WORKDIR /home/$USER


# ###haskell
# RUN sudo apt-get install build-essential curl libffi-dev libffi8ubuntu1 libgmp-dev libgmp10 libncurses-dev libncurses5 libtinfo5 -y

# #this seems to be necessary for some things
# RUN sudo apt-get install libgmp3-dev

# # Install ghcup
# ENV BOOTSTRAP_HASKELL_NONINTERACTIVE=1
# RUN bash -c "curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh"
# RUN bash -c "curl -sSL https://get.haskellstack.org/ | sh"

# # Add ghcup to PATH
# ENV PATH=${PATH}:/root/.local/bin
# ENV PATH=${PATH}:/root/.ghcup/bin

# # Install cabal
# RUN bash -c "ghcup upgrade"
# RUN bash -c "ghcup install cabal 3.6.2.0"
# RUN bash -c "ghcup set cabal 3.6.2.0"

# # Install GHC
# RUN bash -c "ghcup install ghc 9.2.8"
# RUN bash -c "ghcup set ghc 9.2.8"

# # Update Path to include Cabal and GHC exports
# RUN bash -c "echo PATH="$HOME/.local/bin:$PATH" >> $HOME/.bashrc"
# RUN bash -c "echo export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH" >> $HOME/.bashrc"
# RUN bash -c "source $HOME/.bashrc"