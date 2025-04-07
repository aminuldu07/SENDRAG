
# Use an official Python runtime as a parent image
FROM yousuf28/python_base:latest

# Set the working directory in the container
WORKDIR /app

# Copy the application files
COPY . .

# Install required system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    openai \
    chromadb \
    pdfplumber \
    sentence-transformers \
    shiny

# Set environment variable for OpenAI API key (Can be overridden at runtime)
# ENV OPENAI_API_KEY="your-api-key-here"

# Expose the port that Shiny uses
EXPOSE 8000

# Command to run the Shiny app
CMD ["shiny", "run", "--reload", "app.py"]
