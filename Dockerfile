FROM alpine:latest

#RUN apk add --update xvfb && -rf /var/cache/apk/*
RUN apk add --update --no-cache python3 xvfb firefox && ln -sf python3 /usr/bin/python && rm -rf /var/cache/apk/*
RUN python -m ensurepip
RUN python -m pip install --upgrade pip
#RUN pip install setuptools pyvirtualdisplay selenium webdriver_manager webdriver-manager typing time pathlib email.mime selenium.webdriver.firefox.options webdriver_manager.firefox mail webpages_drivers

RUN pip install setuptools 
RUN pip install pyvirtualdisplay 
RUN pip install selenium 
RUN pip install webdriver_manager 
RUN pip install webdriver-manager 
RUN pip install typing time 
RUN pip install pathlib     
RUN pip install email.mime 
RUN pip install selenium.webdriver.firefox.options 
RUN pip install webdriver_manager.firefox 
RUN pip install mail webpages_drivers

RUN pip install --no-cache-dir -r requirements.txt

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
