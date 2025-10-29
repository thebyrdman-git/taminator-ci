# Taminator Intelligence - Containerized Deployment
# 
# Provides Taminator Intelligence as a web service
# TAMs can run locally or deploy to shared server

FROM registry.access.redhat.com/ubi9/python-311:latest

LABEL maintainer="jbyrd@redhat.com"
LABEL description="Taminator Intelligence - AI-Augmented TAM Assistant"
LABEL version="2.1.0"

# Switch to root for system packages
USER 0

# Install system dependencies
RUN dnf install -y \
    sqlite \
    && dnf clean all

# Switch back to non-root user
USER 1001

# Set working directory
WORKDIR /app

# Copy Python source
COPY --chown=1001:0 src/taminator /app/taminator

# Copy requirements (if any)
# COPY --chown=1001:0 requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# Create data directory for SQLite database
RUN mkdir -p /app/data && chmod 775 /app/data

# Expose port for web interface (optional)
EXPOSE 8080

# Environment variables
ENV PYTHONPATH=/app
ENV TAMINATOR_DB_PATH=/app/data/intelligence.db

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python3 -c "from taminator.core.database import get_intelligence_database; db = get_intelligence_database(); print('OK')" || exit 1

# Default command: Run IPC bridge in server mode
CMD ["python3", "-m", "taminator.core.ipc_bridge", "server", "--host", "0.0.0.0", "--port", "8080"]

