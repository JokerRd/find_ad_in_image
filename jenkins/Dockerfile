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
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get --assume-yes install ca-certificates curl
RUN install -m 0755 -d /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
RUN chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
RUN echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get update
RUN apt-get --assume-yes install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
RUN usermod -aG docker jenkins
USER jenkins