FROM python:3.10.15-slim
USER root

RUN pip install --upgrade pip setuptools

COPY ./requirements.txt /tmp/requirements.txt
# RUN pip install pyarrow==9.0.0
RUN pip install -r /tmp/requirements.txt --no-cache-dir

RUN mkdir -p /app

COPY . /app

WORKDIR /app

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app_extract_tableview_offline.py"]