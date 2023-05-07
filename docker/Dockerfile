FROM python:3.8-slim
WORKDIR /usr/app

RUN python3 -m pip install --upgrade pip setuptools

COPY . /usr/app/
RUN python3 -m pip install .

ENV PYTHONPATH /usr/app
ENV FLASK_APP /usr/app/perprof_web/app.py

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]
