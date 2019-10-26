FROM docker.rldsoftware.nl/kraken-websocket2db-base:v1
MAINTAINER Robin van Leeuwen <robinvanleeuwen@gmail.com>

ENV APP_SETTINGS='production'

WORKDIR /kraken-websocket2db
RUN mkdir /root/.kraken
COPY db_settings.conf /root/.kraken/
RUN git pull
RUN pip3 install -r requirements.txt
CMD ["python3", "app.py"]
