FROM alpine:latest

COPY crontab /crontab
COPY entry.sh /entry.sh

COPY git_installer.sh /config/

RUN apk add --update --no-cache git python3 xvfb firefox && ln -sf python3 /usr/bin/python && rm -rf /var/cache/apk/*

RUN apk add git

WORKDIR /config
RUN sh /config/git_installer.sh
#RUN git init .
#RUN ls -a /config
#RUN git remote add origin https://github.com/asger-weirsoee/rest-vaccine-tilmelder
#RUN git remote update 
#RUN git fetch 
#RUN ls -a /config
#RUN git checkout -b master 
#RUN git pull origin master 

RUN python -m ensurepip
RUN python -m pip install --upgrade pip
RUN pip install setuptools 
RUN pip install pyvirtualdisplay 
RUN pip install selenium 
RUN pip install webdriver_manager 
RUN pip install webdriver-manager 
RUN pip install typing 
RUN pip install pathlib     
RUN pip install selenium-firefox

RUN pip install --no-cache-dir -r /config/requirements.txt

RUN chmod 775 /entry.sh

RUN /usr/bin/crontab /crontab

CMD ["/entry.sh"]
