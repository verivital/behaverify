FROM ubuntu:22.04
RUN apt update
RUN apt upgrade
RUN apt install python3 -y
RUN apt install pip -y
RUN python3 -m pip install py_trees=2.3.3
RUN python3 -m pip install pandas=2.0.2
RUN apt install graphviz -y
RUN apt install git -y
RUN mkdir behaverify && cd behaverify && git init && \
    git remote add -f origin https://github.com/verivital/behaverify && \
    echo "REPRODUCIBILITY/2023_SEFM/" >> .git/info/sparse-checkout && \
    git pull origin master
RUN chmod -R +x /behaverify/REPRODUCIBILITY/2023_SEFM/*.sh
RUN chmod +x /behaverify/REPRODUCIBILITY/2023_SEFM/nuXmv
