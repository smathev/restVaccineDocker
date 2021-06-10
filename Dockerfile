FROM alpine:latest

RUN mkdir /config

VOLUME /config

RUN apk add --update --no-cache git python3 xvfb firefox && ln -sf python3 /usr/bin/python && rm -rf /var/cache/apk/*

RUN apk add git

WORKDIR /config
RUN git init .
RUN git remote add origin "https://github.com/asger-weirsoee/rest-vaccine-tilmelder"
RUN git remote update
RUN git fetch
RUN git checkout -b master
RUN git pull origin master

#RUN apk add --update xvfb && -rf /var/cache/apk/*
#COPY requirements.txt /config/requirements.txt
RUN python -m ensurepip
RUN python -m pip install --upgrade pip
#RUN pip install setuptools pyvirtualdisplay selenium webdriver_manager webdriver-manager typing time pathlib email.mime selenium.webdriver.firefox.options webdriver_manager.firefox mail webpages_drivers
RUN pip install setuptools 
RUN pip install pyvirtualdisplay 
RUN pip install selenium 
RUN pip install webdriver_manager 
RUN pip install webdriver-manager 
RUN pip install typing 
RUN pip install pathlib     
RUN pip install selenium-firefox

RUN pip install --no-cache-dir -r /config/requirements.txt

COPY crontab /crontab
#COPY config.json /config/config.json
#COPY mail.py /config/mail.py
#COPY main.py /config/main.py
#COPY images /config/images
#COPY subs /config/subs
#COPY webpages_drivers /config/webpages_drivers

COPY entry.sh /entry.sh
#RUN chmod 755 /config/main.py /config/mail.py /config/config.json /entry.sh
RUN /usr/bin/crontab /crontab

VOLUME /config

CMD ["/entry.sh"]
