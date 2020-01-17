# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM python:3.6-slim-buster
# Update OS
RUN apt-get update -y
# Copy file
COPY . .
# Install environment
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
# Add permision script
RUN chmod +x start_request.sh
# Folder to run script
ENTRYPOINT ["/bin/bash"]
# Trigger Python script
CMD ["start_request.sh"]