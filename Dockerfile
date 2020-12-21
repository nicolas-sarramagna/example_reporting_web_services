FROM python:3.6.12-slim-buster

ENV WORKDIR=/usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}"

WORKDIR $WORKDIR

COPY . $WORKDIR

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python","./example_reporting_web_services/app_ws.py"]

