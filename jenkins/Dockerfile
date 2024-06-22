FROM jenkins/jenkins:lts
USER root
RUN apt-get update
RUN apt-get --assume-yes install python3 wget
RUN wget -O get-pip.py https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py --break-system-packages
RUN touch /etc/pip.conf
RUN echo "[global]" >> /etc/pip.conf
RUN echo "break-system-packages = true" >> /etc/pip.conf
RUN ln -s /bin/python3 /bin/python
RUN python -m pip install flake8 pytest
USER jenkins