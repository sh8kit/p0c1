FROM python:3.9
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# install terraform
RUN apt-get install unzip -y
RUN wget https://releases.hashicorp.com/terraform/1.3.6/terraform_1.3.6_linux_amd64.zip
RUN unzip terraform_1.3.6_linux_amd64.zip
RUN mv terraform /usr/local/bin/


# Install supervisor
RUN pip install supervisor


RUN mkdir /datashack
WORKDIR /datashack
COPY . .
RUN python -m pip install -r requirements.txt
EXPOSE 8501 5000
CMD ["supervisord","-c","service_script.config"]
