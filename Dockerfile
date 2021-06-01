FROM alpine:latest

RUN apk add --update xvfb && rm -rf /var/cache/apk/*

COPY crontab /crontab
COPY config.json /config/config.json
COPY mail.py /config/mail.py
COPY main.py /config/main.py
COPY images /config/images
COPY subs /config/subs
COPY webpages_drivers /config/webpages_drivers
COPY entry.sh /entry.sh
RUN chmod 755 /config/main.py /config/mail.py /config/config.json /entry.sh
RUN /usr/bin/crontab /crontab

VOLUME /config

CMD ["/entry.sh"]
