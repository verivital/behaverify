FROM ubuntu:23.10
RUN apt-get update -y \
    && apt-get upgrade -y

# Set the non-root user information
ARG USER=behaverify
ARG UID=16228
ARG GID=16228

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
RUN echo /src >> /home/$USER/behaverify/.git/info/sparse-checkout
RUN echo /metamodel >> /home/$USER/behaverify/.git/info/sparse-checkout
RUN echo /Docker_BehaVerify/util >> /home/$USER/behaverify/.git/info/sparse-checkout
RUN echo /requirements >> /home/$USER/behaverify/.git/info/sparse-checkout
RUN echo /scripts/nuxmv_commands >> /home/$USER/behaverify/.git/info/sparse-checkout
RUN echo /demos >> /home/$USER/behaverify/.git/info/sparse-checkout
RUN git checkout
RUN chmod -R +x /home/$USER/behaverify/Docker_BehaVerify/util/*.sh
RUN python3 -m venv /home/$USER/behaverify_venv
RUN /home/$USER/behaverify_venv/bin/python3 -m pip install --upgrade pip
RUN /home/$USER/behaverify_venv/bin/python3 -m pip install -r /home/$USER/behaverify/requirements/core.txt
RUN python3 -m venv /home/$USER/draw_venv
RUN /home/$USER/draw_venv/bin/python3 -m pip install --upgrade pip
RUN /home/$USER/draw_venv/bin/python3 -m pip install -r /home/$USER/behaverify/requirements/drawing.txt
RUN mkdir /home/$USER/user_files

WORKDIR /home/$USER
