# Use a slim Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some image libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements/project definition
COPY pyproject.toml .

# Install uv for fast dependency management
RUN pip install uv

# Install dependencies using uv
# We create a virtual environment or install into system python in container
RUN uv pip install --system -r pyproject.toml

# Copy the rest of the application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Default command: Run the Feature Extractor? Or the App?
# We'll use a bash shell so the user can run commands, or a custom entrypoint.
# Let's default to a helpful shell message.
CMD ["/bin/bash"]
