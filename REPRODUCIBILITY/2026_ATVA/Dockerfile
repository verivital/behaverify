FROM ubuntu:24.04
RUN apt-get update -y
RUN apt-get upgrade -y

# Set the non-root user information
ARG VENUE=2026_ATVA
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

WORKDIR /home/$USER
USER $USER

RUN sudo apt-get install wget git python3 pip python3-venv python3-tk -y
RUN sudo apt-get install graphviz -y

ADD https://api.github.com/repos/verivital/behaverify/git/refs/heads/main version.json
# this makes sure we grab the newest version of the repo instead of reusing an older one

RUN git clone --filter=blob:none --no-checkout --depth 1 --sparse https://github.com/verivital/behaverify
WORKDIR /home/$USER/behaverify
RUN git sparse-checkout set --no-cone
RUN echo !/* > /home/$USER/behaverify/.git/info/sparse-checkout
RUN echo /REPRODUCIBILITY/$VENUE >> /home/$USER/behaverify/.git/info/sparse-checkout
RUN git checkout

RUN python3 -m venv /home/$USER/python_venvs/behaverify
RUN /home/$USER/python_venvs/behaverify/bin/python3 -m pip install --upgrade pip
RUN /home/$USER/python_venvs/behaverify/bin/python3 -m pip install behaverify
RUN /home/$USER/python_venvs/behaverify/bin/python3 -m pip install -r /home/$USER/behaverify/REPRODUCIBILITY/$VENUE/requirements/core.txt

ENV PATH="/home/BehaVerify_2026_ATVA/python_venvs/behaverify/bin:$PATH"

WORKDIR /home/$USER/behaverify/REPRODUCIBILITY/$VENUE

CMD ["/bin/bash", "-c", "./BehaVerify_2026_ATVA.sh ./"]
