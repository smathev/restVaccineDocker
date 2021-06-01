FROM python:3-alpine

RUN python -m pip install --upgrade pip
RUN pip install selenium

COPY crontab /crontab
COPY locations.py /config/locations.py
COPY variables.py /config/variables.py
COPY vaccine_script.py /config/vaccine_script.py
COPY entry.sh /entry.sh
RUN chmod 755 /config/locations.py /config/variables.py /config/vaccine_script.py /entry.sh
RUN /usr/bin/crontab /crontab

VOLUME /config

CMD ["/entry.sh"]
