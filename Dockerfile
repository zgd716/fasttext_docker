FROM joelogan/keras-tensorflow-flask-uwsgi-nginx-docker
COPY ./app /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt