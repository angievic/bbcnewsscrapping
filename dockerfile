FROM python:3
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD bbcnews.py /
CMD [ "python", "./bbcnews.py" ]