FROM python:3.11-slim

# We copy just the requirements.txt first to leverage Docker cache


WORKDIR /app
COPY ../notebook_proxy/ /app
#COPY ./requirements_mknb.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

ENV FLASK_APP=mknb


ENTRYPOINT [ "python3" ]

CMD [ "mknb.py" ]
