# Docker Deployment Guide

## Quick Start

```bash
# Clone the repository
git clone https://github.com/neosun100/pdf2ppt.git
cd pdf2ppt

# Start the service
./start.sh
```

Access the service at: http://localhost:8000

## Using Docker Hub Image

```bash
# Pull the image
docker pull neosun/pdf2ppt:latest

# Run the container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/uploads:/tmp/pdf2ppt/uploads \
  -v $(pwd)/outputs:/tmp/pdf2ppt/outputs \
  --name pdf2ppt \
  neosun/pdf2ppt:latest
```

## Docker Compose

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Restart
docker-compose restart
```

## Environment Variables

Create a `.env` file:

```bash
PORT=8000
DEFAULT_PARALLEL_WORKERS=4
MAX_FILE_SIZE_MB=100
```

## Volume Mounts

| Container Path | Purpose | Recommended Host Path |
|----------------|---------|----------------------|
| `/tmp/pdf2ppt/uploads` | Uploaded PDF files | `./uploads` |
| `/tmp/pdf2ppt/outputs` | Converted PPTX files | `./outputs` |

## Accessing the Service

### Web UI
- URL: http://localhost:8000
- Features: Drag-and-drop upload, real-time progress, multi-language support

### API Documentation
- URL: http://localhost:8000/docs
- Interactive Swagger UI with all endpoints

### Health Check
- URL: http://localhost:8000/health
- Returns: `{"status": "healthy", "version": "1.2.0"}`

## API Usage Examples

### Convert a PDF

```bash
curl -X POST "http://localhost:8000/api/convert" \
  -F "file=@slides.pdf" \
  -F 'options={"pages":"1-10","parallel":4}'
```

### Download converted file

```bash
curl -O "http://localhost:8000/api/download/slides.pptx"
```

## Building Custom Image

```bash
# Build
docker build -t my-pdf2ppt .

# Run
docker run -d -p 8000:8000 my-pdf2ppt
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs pdf2ppt

# Check if port is in use
lsof -i :8000
```

### Permission issues

```bash
# Fix volume permissions
chmod -R 777 uploads outputs
```

### Out of memory

```bash
# Increase Docker memory limit
docker run -d -p 8000:8000 -m 2g neosun/pdf2ppt:latest
```

## Production Deployment

### Using Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name pdf2ppt.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Using Docker Swarm

```bash
docker service create \
  --name pdf2ppt \
  --replicas 3 \
  --publish 8000:8000 \
  neosun/pdf2ppt:latest
```

### Using Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pdf2ppt
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pdf2ppt
  template:
    metadata:
      labels:
        app: pdf2ppt
    spec:
      containers:
      - name: pdf2ppt
        image: neosun/pdf2ppt:latest
        ports:
        - containerPort: 8000
```

## Monitoring

### Health Checks

```bash
# Docker health check
docker inspect --format='{{.State.Health.Status}}' pdf2ppt

# Manual check
curl http://localhost:8000/health
```

### Resource Usage

```bash
# Container stats
docker stats pdf2ppt

# Detailed info
docker inspect pdf2ppt
```

## Backup and Restore

### Backup outputs

```bash
tar -czf outputs-backup.tar.gz outputs/
```

### Restore outputs

```bash
tar -xzf outputs-backup.tar.gz
```

## Security

### Run as non-root user

```dockerfile
USER nobody
```

### Limit resources

```yaml
services:
  pdf2ppt:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### Network isolation

```yaml
services:
  pdf2ppt:
    networks:
      - internal
networks:
  internal:
    internal: true
```

## Support

- GitHub: https://github.com/neosun100/pdf2ppt
- Docker Hub: https://hub.docker.com/r/neosun/pdf2ppt
- Issues: https://github.com/neosun100/pdf2ppt/issues
