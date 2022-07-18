FROM python:3
WORKDIR /src/app
COPY ./ /src/app
RUN python3 -m pip install -r requirements.txt
CMD [ "streamlit", "run", "app.py" ]
