FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE ${STREAMLIT_SERVER_PORT}
CMD ["streamlit", "run", "app.py"]