FROM python 
COPY ./* /spreader
RUN pip install -r /spreader/requirements.txt

ENTRYPOINT cd /spreader && python spreading_handler.py