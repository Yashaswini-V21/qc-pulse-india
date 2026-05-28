# Deployment Guide

## Local Deployment

### 1. Production Setup

```bash
# Clone repository
git clone https://github.com/Yashaswini-V21/qc-pulse-india.git
cd qc-pulse-india

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app.py
```

### 2. Performance Optimization

#### Streamlit Configuration
Create `.streamlit/config.toml`:
```toml
[client]
showErrorDetails = false

[server]
port = 8501
headless = true
runOnSave = false

[logger]
level = "warning"
```

---

## Cloud Deployment (Streamlit Cloud)

### Prerequisites
- GitHub account with repository
- Streamlit account (connect to GitHub)

### Steps

1. **Push to GitHub:**
```bash
git push origin main
```

2. **Deploy on Streamlit Cloud:**
- Visit: https://share.streamlit.io/
- Click "New app" → Select repository
- Branch: `main`
- Main file path: `app.py`
- Deploy!

### Environment Variables
Add secrets in Streamlit Cloud dashboard:
```
[secrets]
DB_PASSWORD = "your_password_here"
API_KEY = "your_api_key_here"
```

---

## Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8501

# Run streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

### 2. Create .dockerignore

```
data/raw/
outputs/
.git
.github
__pycache__
.env
.venv
*.log
```

### 3. Build & Run

```bash
# Build image
docker build -t qc-pulse-india .

# Run container
docker run -p 8501:8501 qc-pulse-india

# Push to Docker Hub
docker tag qc-pulse-india:latest your-username/qc-pulse-india:latest
docker push your-username/qc-pulse-india:latest
```

---

## Heroku Deployment

### 1. Create Procfile

```
web: streamlit run app.py --server.port=$PORT
```

### 2. Create runtime.txt

```
python-3.10.5
```

### 3. Deploy

```bash
# Login to Heroku
heroku login

# Create app
heroku create qc-pulse-india

# Deploy
git push heroku main

# Monitor
heroku logs --tail
```

---

## AWS Deployment

### Using EC2

1. **Launch EC2 instance** (Ubuntu 20.04 or later)

2. **Connect and setup:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python & dependencies
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/Yashaswini-V21/qc-pulse-india.git
cd qc-pulse-india

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run Streamlit
streamlit run app.py --server.port 80
```

3. **Configure Security Group:**
- Inbound: Allow port 80 (HTTP), 22 (SSH)
- Outbound: Allow all

---

## Azure Deployment

### Using Azure App Service

```bash
# Login to Azure
az login

# Create resource group
az group create --name qc-pulse-india-rg --location eastus

# Create App Service
az appservice plan create --name qc-pulse-plan --resource-group qc-pulse-india-rg --sku F1 --is-linux

# Deploy
az webapp create --resource-group qc-pulse-india-rg --plan qc-pulse-plan --name qc-pulse-india --runtime "PYTHON|3.10"

# Configure & deploy
git push azure main
```

---

## Google Cloud Deployment

### Using Cloud Run

```bash
# Authenticate
gcloud auth login

# Create Dockerfile (see Docker section above)

# Deploy
gcloud run deploy qc-pulse-india --source . --platform managed --region us-central1 --allow-unauthenticated
```

---

## Monitoring & Maintenance

### Health Checks
```bash
# Test dashboard
curl http://localhost:8501

# Check logs
tail -f streamlit_app.log
```

### Backup Strategy
```bash
# Backup data files
tar -czf qc-pulse-backup-$(date +%Y%m%d).tar.gz data/ notebooks/

# Store in cloud (S3, Azure Blob, GCS, etc.)
```

### Update Procedure
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Restart app
# Kill existing process and restart
```

---

## Troubleshooting Deployments

### Port Issues
```bash
# Check if port is in use
lsof -i :8501

# Kill process
kill -9 <PID>
```

### Memory Issues
```bash
# Monitor memory usage
watch -n 1 free -h

# Increase if needed (cloud providers allow scaling)
```

### Data Access
Ensure data files are:
- In `data/clean/` directory
- Readable by app process
- Small enough to load in memory

---

## Security Considerations

- Never commit `.env` or `secrets.json`
- Use environment variables for sensitive data
- Enable authentication for production
- Keep dependencies updated
- Use HTTPS/TLS for connections
- Implement rate limiting
- Add monitoring & alerting

---

## Performance Benchmarks

| Metric | Local | Cloud |
|--------|-------|-------|
| **Load Time** | 2-3s | 3-5s |
| **Page Switch** | <200ms | <500ms |
| **Memory** | ~200MB | ~256MB+ |
| **CPU** | Variable | Shared |

---

## Support

- 📧 Email: yashasyashu0987@gmail.com
- 🐛 Issues: GitHub Issues
- 📖 Docs: README & data_schema.md
