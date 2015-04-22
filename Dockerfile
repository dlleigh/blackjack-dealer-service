FROM debian

RUN apt-get -qq update && \
        apt-get -y --force-yes install \
        ant \
        bash \
        build-essential \
        curl \
        dnsutils \
        git-core \
        less \
        python-pip \
        wget

#Python
RUN pip install behave
RUN pip install coverage
RUN pip install flask
RUN pip install requests
RUN pip install mock
RUN pip install ipdb

# Set work dir

COPY . /opt/blackjack-dealer-service

WORKDIR /opt/blackjack-dealer-service

EXPOSE 5000

CMD    [python BlackjackService.py]
