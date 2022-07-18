FROM python:3
ADD app.py /
ADD requirements.txt /
RUN python3 -m pip install -r requirements.txt
CMD [ "streamlit", "run", "app.py" ]
