FROM python:3-alpine

RUN apk update && apk add --no-cache bash \
        alsa-lib \
        at-spi2-atk \
        atk \
        cairo \
        cups-libs \
        dbus-libs \
        eudev-libs \
        expat \
        flac \
        gdk-pixbuf \
        glib \
        libgcc \
        libjpeg-turbo \
        libpng \
        libwebp \
        libx11 \
        libxcomposite \
        libxdamage \
        libxext \
        libxfixes \
        tzdata \
        libexif \
        udev \
        xvfb \
        zlib-dev \
        chromium \
        chromium-chromedriver

RUN python -m pip install --upgrade pip
RUN pip install selenium
RUN pip install chromedriver-py


COPY crontab /crontab
COPY locations.py /config/locations.py
COPY variables.py /config/variables.py
COPY vaccine_script.py /config/vaccine_script.py
COPY entry.sh /entry.sh
RUN chmod 755 /config/locations.py /config/variables.py /config/vaccine_script.py /entry.sh
RUN /usr/bin/crontab /crontab

VOLUME /config

CMD ["/entry.sh"]
