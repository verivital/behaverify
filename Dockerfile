FROM ubuntu:22.04
RUN apt update
RUN apt install python3 -y
RUN apt install pip -y
RUN python3 -m pip install py_trees
RUN python3 -m pip install pandas
RUN apt install graphviz -y
RUN apt install git -y
RUN git clone https://github.com/verivital/behaverify.git
RUN mv /behaverify /root/behaverify
RUN cp /root/behaverify/scripts/minimal_script.sh /minimal_script.sh
RUN cp /root/behaverify/scripts/nuXmv ~/nuXmv
RUN chmod +x /minimal_script.sh
RUN chmod -R +x /root/behaverify/examples/.
RUN chmod +x ~/nuXmv
