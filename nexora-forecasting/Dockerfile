# pull the base image
FROM python:3.11-slim

# create working directory
WORKDIR /app

# copy requirments.txt into the root of our working directory
COPY requirements.txt .

# install dependencies without cache
RUN pip install --no-cache-dir -r requirements.txt

# copy everyother thing
COPY . .

# expose docker port
EXPOSE 8000

# command that runs the project
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

