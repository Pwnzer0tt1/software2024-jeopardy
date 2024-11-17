FROM python:3.12

RUN mkdir -p /execute
WORKDIR /execute

ADD ./requirements.txt /execute/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /execute/requirements.txt --no-warn-script-location

COPY ./ /execute/

RUN useradd -ms /bin/sh rooot
RUN chmod -R og-w /execute
RUN chmod -R og+r /execute
RUN chmod ugo+x ./shell

ENV FLAG1="FLAG{S3creTTTT_POST_r3quest}"
ENV FLAG2="FLAG{Encoded_HTTP_Header_!_🥶}"
ENV FLAG3="FLAG{cats>>>>>>>_json_encoding}"

RUN python3 /execute/app.py docker
CMD ["uwsgi", "--http", ":5000", "--wsgi-file", "app.py", "--callable", "app", "--thunder-lock", "--enable-threads", "--max-fd", "1024"]


