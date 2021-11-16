FROM python

# We copy just the requirements.txt first to leverage Docker cache


WORKDIR /app
COPY ../src/notebook_proxy/ /app
#COPY ./requirements_mknb.txt /app/requirements.txt
RUN pip3 install -r requirements.txt



ENTRYPOINT [ "python3" ]

CMD [ "mknb.py" ]