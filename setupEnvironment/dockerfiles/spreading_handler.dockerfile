FROM python:3.7-alpine
COPY ./src /spreader/
RUN pip install -r /spreader/requirements.txt

ENTRYPOINT cd /spreader && python spreading_handler.py