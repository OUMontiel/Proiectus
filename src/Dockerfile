FROM tiangolo/uvicorn-gunicorn:python3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

CMD [ "uvicorn", "main:app", "--host=0.0.0.0", "--reload" ]