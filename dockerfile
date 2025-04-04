FROM alpine:latest

# Install Python & pip
RUN apk add --no-cache python3 py3-pip

# Create a user
RUN adduser -D app

# Switch to the new user
USER app
WORKDIR /home/app

# create project environemnt
RUN python3 -m venv /home/app/env

# Copy dependencies first for caching
COPY --chown=app:app requirements.txt .

# Copy application code
COPY --chown=app:app ./src ./src

# Install dependencies
RUN /home/app/env/bin/pip install --no-cache-dir -r requirements.txt

# Expose the necessary port
EXPOSE 8000

# Define a volume for logs
VOLUME [ "/home/app/logs" ]

# Run the application with virtual env
CMD [ "/home/app/env/bin/python", "./src/main.py" ]
