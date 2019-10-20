FROM alpine:latest
MAINTAINER Robin van Leeuwen <robinvanleeuwen@gmail.com>
RUN apk add python3 g++ make postgresql-libs libffi-dev python3-dev
RUN git clone https://github.com/robinvanleeuwen/kraken-websocket2db.git
RUN cd kraken-websocker2db; pip3 install -r requirements.txt
CMD ["cd kraken-websocket2db; python3 app.py"]
