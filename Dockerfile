FROM alpine:latest

RUN apk add --update xorg-server-xvfb && rm -rf /var/cache/apk/*

COPY crontab /crontab
COPY config.json /config/config.json
COPY mail.py /config/mail.py
COPY vaccine_main.py /config/mail.py
COPY images /config/images
COPY subs /config/subs
COPY webpages_drivers /config/webpages_drivers
COPY entry.sh /entry.sh
RUN chmod 755 /config/locations.py /config/variables.py /config/vaccine_script.py /entry.sh
RUN /usr/bin/crontab /crontab

VOLUME /config

CMD ["/entry.sh"]
