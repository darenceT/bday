FROM python:3.9-slim-buster
RUN pip3 install flask flask-wtf email_validator requests werkzeug flask_sqlalc>
COPY bday/ bday/
CMD python bday/bday.py