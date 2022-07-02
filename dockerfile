FROM ubuntu:22.04
RUN apt update
RUN apt upgrade
RUN apt install python3
RUN apt install pip
RUN python3 -m install py_trees
RUN python3 -m install pandas
RUN apt install graphviz
RUN apt install git
RUN git clone https://github.com/verivital/behaverify.git
RUN mv /behaverify /root/behaverify
RUN cp /root/behaverify/scripts/minimal_script.sh /minimal_script.sh
RUN cp /root/behaverify/scripts/nuXmv ~/nuXmv
RUN chmod +x /minimal_script.sh
RUN chmod -R +x /root/behaverify/examples/.
