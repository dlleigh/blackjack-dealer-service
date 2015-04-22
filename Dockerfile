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
RUN pip install behave coverage flask requests mock ipdb

# Set work dir

COPY . /opt/blackjack-dealer-service

WORKDIR /opt/blackjack-dealer-service

EXPOSE 5000

CMD    ["/usr/bin/python", "BlackjackDealerService.py"]
