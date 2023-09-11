FROM ubuntu:22.04
RUN apt update -y
RUN apt upgrade -y
#RUN apt install sudo -y
#RUN useradd -u 1234 theUser
#USER theUser

RUN apt install python3 -y
RUN apt install pip -y
RUN python3 -m pip install py_trees
RUN python3 -m pip install pandas
RUN python3 -m pip install jinja2
RUN python3 -m pip install textx
RUN python3 -m pip install matplotlib
RUN apt install graphviz -y
RUN apt install git -y

RUN apt install build-essential curl libffi-dev libffi8ubuntu1 libgmp-dev libgmp10 libncurses-dev libncurses5 libtinfo5 -y

#this seems to be necessary for some things
RUN apt install libgmp3-dev

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
    echo "REPRODUCIBILITY/2023_SEFM/" >> .git/info/sparse-checkout && \
    git pull origin main
RUN chmod -R +x /behaverify/REPRODUCIBILITY/2023_SEFM/*.sh
#RUN chmod +x /behaverify/REPRODUCIBILITY/2023_SEFM/nuXmv
