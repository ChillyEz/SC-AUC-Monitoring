# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Clone and Setup
```bash
git clone https://github.com/ChillyEz/SC-AUC-Monitoring.git
cd SC-AUC-Monitoring
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure
```bash
cp .env.example .env
# Edit .env if needed (default settings work for demo)
```

### 3. Run
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the script:
```bash
cd ..
./scripts/run_dev.sh
```

### 4. Access
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs  
- **Health**: http://localhost:8000/health

## 📚 What's Next?

### Testing Stalcraft API
1. Get a valid item ID from Stalcraft
2. Edit `scripts/test_api.py`:
   ```python
   REGION = "EU"
   ITEM_ID = "your_real_item_id"
   ```
3. Run: `python scripts/test_api.py`
4. Check results in `docs/auction_*_example_*.json`
5. Adapt models in `backend/app/models/auction.py` based on real data

### Docker
```bash
cd docker
docker-compose up
```

### Read Documentation
- [Architecture](docs/ARCHITECTURE.md) - Understand the structure
- [Development](docs/DEVELOPMENT.md) - Developer guide
- [API](docs/API.md) - API reference
- [Stalcraft API](docs/STALCRAFT_API.md) - Integration guide

## 🎯 MVP Status

✅ **Complete** - All Stage 1 requirements implemented  
⏳ **Next** - Test with real Stalcraft API and adapt models

## 📞 Support

Issues: https://github.com/ChillyEz/SC-AUC-Monitoring/issues
