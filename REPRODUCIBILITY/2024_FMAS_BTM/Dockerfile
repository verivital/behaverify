FROM ubuntu:23.10
RUN apt-get update -y \
    && apt-get upgrade -y

# Set the non-root user information
ARG VENUE=2024_FMAS_BTM
ARG USER=BehaVerify_$VENUE
ARG UID=18281
ARG GID=18281

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

# Hyperfine installation!
RUN sudo apt-get install wget -y
RUN wget https://github.com/sharkdp/hyperfine/releases/download/v1.16.1/hyperfine_1.16.1_amd64.deb
RUN sudo dpkg -i hyperfine_1.16.1_amd64.deb

# jq installation!
RUN sudo apt-get install jq -y

# Copilot installation!
RUN sudo apt-get install g++ cmake -y
RUN sudo apt-get install libghc-copilot-dev -y

# LTL2BA installation!
RUN sudo apt-get install g++ cmake make git autoconf libconfig-dev libtool -y

ADD https://api.github.com/repos/utwente-fmt/ltl2ba/git/refs/heads/master version.json
RUN git clone https://github.com/utwente-fmt/ltl2ba

WORKDIR /home/$USER/ltl2ba
RUN autoupdate
RUN autoreconf --install --force
RUN ./configure
RUN make

WORKDIR /home/$USER

# BehaVerify Installation!
RUN sudo apt-get install git -y
RUN sudo apt-get install python3 pip python3-venv -y

# ADD https://api.github.com/repos/$USER/$REPO/git/refs/heads/$BRANCH version.json
ADD https://api.github.com/repos/verivital/behaverify/git/refs/heads/main version.json

RUN git clone --filter=blob:none --no-checkout --depth 1 --sparse https://github.com/verivital/behaverify
WORKDIR /home/$USER/behaverify
RUN git sparse-checkout set --no-cone
RUN echo !/* > /home/$USER/behaverify/.git/info/sparse-checkout
RUN echo /REPRODUCIBILITY/$VENUE >> /home/$USER/behaverify/.git/info/sparse-checkout
RUN git checkout

RUN chmod -R +x /home/$USER/behaverify/REPRODUCIBILITY/$VENUE/*.sh

RUN python3 -m venv /home/$USER/python_venvs/behaverify
RUN /home/$USER/python_venvs/behaverify/bin/python3 -m pip install --upgrade pip
RUN /home/$USER/python_venvs/behaverify/bin/python3 -m pip install -r /home/$USER/behaverify/REPRODUCIBILITY/$VENUE/requirements/core.txt
RUN python3 -m venv /home/$USER/python_venvs/results
RUN /home/$USER/python_venvs/results/bin/python3 -m pip install --upgrade pip
RUN /home/$USER/python_venvs/results/bin/python3 -m pip install -r /home/$USER/behaverify/REPRODUCIBILITY/$VENUE/requirements/results.txt

WORKDIR /home/$USER
