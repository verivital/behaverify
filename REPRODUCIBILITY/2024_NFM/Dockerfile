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



RUN apt-get install python3 -y
RUN apt-get install pip -y
ENV PIP_ROOT_USER_ACTION=ignore
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install py_trees
RUN python3 -m pip install pandas
RUN python3 -m pip install textx
RUN python3 -m pip install matplotlib
RUN python3 -m pip install jinja2
#jinja2 is needed for dataframe in processing results
RUN sudo apt-get install graphviz -y
RUN sudo apt-get install git -y

# RUN sudo apt-get install build-essential curl libffi-dev libffi8ubuntu1 libgmp-dev libgmp10 libncurses-dev libncurses5 libtinfo5 -y

# RUN sudo apt-get install libgmp3-dev -y

RUN mkdir behaverify && cd behaverify && git init && \
    git remote add -f origin https://github.com/verivital/behaverify && \
    echo "REPRODUCIBILITY/2024_NFM/" >> .git/info/sparse-checkout && \
    git pull origin main
RUN chmod -R +x /behaverify/REPRODUCIBILITY/2024_NFM/*.sh
