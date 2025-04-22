FROM ubuntu:24.04
RUN apt-get update -y
RUN apt-get upgrade -y

# Set the non-root user information
ARG VENUE=BT2Fiacre
ARG USER=BT2Fiacre
ARG UID=28337
ARG GID=28337

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

RUN sudo apt-get install wget git curl -y
#^ for downloading.
RUN sudo apt-get install cmake build-essential -y
#^ for configuration?
RUN sudo apt-get install pkg-config autoconf automake -y
#^ for configuration?
RUN sudo apt-get install libtool -y
#^ for configuration?
RUN sudo apt-get install flex bison -y
#^ required by genom3, which seems to be required by bt2fiacre?
RUN sudo apt-get install tcl-dev tk-dev mesa-common-dev libjpeg-dev libtogl-dev -y
#^ also seems required by genom3????
RUN sudo apt-get install libtirpc-dev -y
#^ required by pocolib

# TINA
WORKDIR /home/$USER
RUN wget https://projects.laas.fr/tina/binaries/tina-3.7.5-amd64-linux.tgz
RUN tar -xf tina-3.7.5-amd64-linux.tgz
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/$USER/tina-3.7.5/lib
ENV TINA_DIST=/home/$USER/tina-3.7.5
ENV PATH=$PATH:/home/$USER/tina-3.7.5/bin

# HIPPO/FRAC
WORKDIR /home/$USER
RUN wget https://projects.laas.fr/hippo/binaries/hippo-2.7.1-amd64-linux.tgz
RUN tar -xf hippo-2.7.1-amd64-linux.tgz
RUN sed -i "s/FRACLIB=.*/FRACLIB=\/home\/$USER\/hippo-2.7.1\/lib/g" /home/$USER/hippo-2.7.1/Makefile
ENV PATH=$PATH:/home/$USER/hippo-2.7.1
ENV HIPPO_DIST=/home/$USER/hippo-2.7.1

# GENOM3
WORKDIR /home/$USER
RUN wget https://www.openrobots.org/distfiles/genom/genom-2.99.44.tar.gz
RUN tar -xf genom-2.99.44.tar.gz
WORKDIR /home/$USER/genom-2.99.44
RUN sudo chmod +x "/home/$USER/genom-2.99.44/configure"
RUN bash -c "/home/$USER/genom-2.99.44/configure"
RUN sudo make install

# POCOLIBS
WORKDIR /home/$USER
RUN wget http://www.openrobots.org/distfiles/pocolibs/pocolibs-2.13.tar.gz
RUN tar -xf pocolibs-2.13.tar.gz
WORKDIR /home/$USER/pocolibs-2.13
RUN sudo chmod +x "/home/$USER/pocolibs-2.13/configure"
RUN /home/$USER/pocolibs-2.13/configure
# RUN make #THIS LINE BROKEN BECAUE OF rpc/rpc.h
# RUN sudo make install


# BT2FIACRE
WORKDIR /home/$USER
RUN git clone git://redmine.laas.fr/laas/users/felix/bt2fiacre.git
WORKDIR /home/$USER/bt2fiacre
RUN sudo chmod +x "/home/$USER/bt2fiacre/bootstrap.sh"
# RUN bash -c "/home/$USER/bt2fiacre/bootstrap.sh || true"
# RUN bash -c "cp /home/$USER/bt2fiacre/src/config-ac.h.in /home/$USER/bt2fiacre/src/config.h.in"
RUN sed -i '/src\/config.h/d' "/home/$USER/bt2fiacre/configure.ac"
RUN sed -i 's/src\/config-ac.h/src\/config.h/g' "/home/$USER/bt2fiacre/configure.ac"
RUN bash -c "/home/$USER/bt2fiacre/bootstrap.sh"
RUN bash -c "/home/$USER/bt2fiacre/configure"
RUN sudo make install

# Set the working directory
WORKDIR /home/$USER


# INSTALLATION
# ------------

# - Download then unpack the adequate frac distribution; this creates a folder
#   frac-X.Y.Z, let FRACDIR be its full path;

# - Set the value of variable FRACLIB in FRACDIR/Makefile to FRACDIR/lib;

# - Add directory FRACDIR to your PATH environment variable;

# - FRACDIR/doc holds the frac manual page in various formats.
#   On unixes, you may wish to add FRACDIR/doc/man to your MANPATH environment variable.


# 2. installing the toolbox:
# --------------------------

# Download and  unpack the tina  distribution. This creates  a hierarchy
# rooted  at tina-3.X.Y.   The binaries  are in  subdirectory  bin.  The
# editor  is "nd".

# The man pages are in  doc/man/mann, a quick installation in tcsh is e.g.
# 	setenv MANPATH <tinadir>/doc/man:$MANPATH
# Directory doc/txt holds text only copies of these.

# To  use  the tools  standalone,  you  may wish  to  add  the tina  bin
# directory to the PATH environment variable, and the tina lib directory
# (if any) to  variable LD_LIBRARY_PATH. This is not  required for using
# the tools from  the editor, however.  Alternatively, nd  and the tools
# can  be  moved or  copied  at  some  standard place  (e.g.   /usr/bin)
# provided all the contents of the tina bin directory is moved or copied
# there. Similarly, the libraries could be moved to /usr/lib and the man
# pages to /usr/man/mann.

# The nd  graphic editor assumes  a 3-button mouse is  present. Bindings
# for  emulating a  3-button  mouse with  a  2-button mouse  or pad  are
# built-in: the  Middle button is simulated  by Shift-RightButton. Click
# Help->nd help for information on the graphic bindings.