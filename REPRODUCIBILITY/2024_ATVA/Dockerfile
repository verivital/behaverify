FROM ubuntu:22.04
RUN apt-get update -y
RUN apt-get upgrade -y

# Set the non-root user information
ARG USER=2024_ATVA_BehaVerify
ARG UID=43719
ARG GID=43719

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

# ADD https://api.github.com/repos/$USER/$REPO/git/refs/heads/$BRANCH version.json
ADD https://api.github.com/repos/verivital/behaverify/git/refs/heads/main version.json

RUN git clone --filter=blob:none --no-checkout --depth 1 --sparse https://github.com/verivital/behaverify
WORKDIR /home/$USER/behaverify
RUN git sparse-checkout set --no-cone
RUN echo !/* > /home/$USER/behaverify/.git/info/sparse-checkout
RUN echo /REPRODUCIBILITY/2024_ATVA >> /home/$USER/behaverify/.git/info/sparse-checkout
RUN git checkout

RUN chmod -R +x /home/$USER/behaverify/REPRODUCIBILITY/2024_ATVA/*.sh
RUN chmod -R +x /home/$USER/behaverify/REPRODUCIBILITY/2024_ATVA/scripts/build_scripts/*.sh
RUN chmod -R +x /home/$USER/behaverify/REPRODUCIBILITY/2024_ATVA/scripts/encoding_timing_scripts/*.sh
RUN chmod -R +x /home/$USER/behaverify/REPRODUCIBILITY/2024_ATVA/scripts/process_results_scripts/*.sh
RUN chmod -R +x /home/$USER/behaverify/REPRODUCIBILITY/2024_ATVA/scripts/test_scripts/*.sh

RUN python3 -m venv /home/$USER/python_venvs/behaverify
RUN /home/$USER/python_venvs/behaverify/bin/python3 -m pip install -- upgrade pip
RUN /home/$USER/python_venvs/behaverify/bin/python3 -m pip install -r /home/$USER/behaverify/REPRODUCIBILITY/2024_ATVA/requirements/core.txt
RUN python3 -m venv /home/$USER/python_venvs/results
RUN /home/$USER/python_venvs/results/bin/python3 -m pip install -- upgrade pip
RUN /home/$USER/python_venvs/results/bin/python3 -m pip install -r /home/$USER/behaverify/REPRODUCIBILITY/2024_ATVA/requirements/results.txt

WORKDIR /home/$USER
