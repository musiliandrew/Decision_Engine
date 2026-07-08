# Start Decision Engine Locally

Open a terminal and navigate to the `decision-engine` directory:
```bash
cd ~/Desktop/Projects/CareerScoper/decision-engine
```

Create and activate a virtual environment (only needed once):
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the FastAPI server:
```bash
uvicorn api:app --host 0.0.0.0 --port 8003 --reload
```
This service will run on **Port 8003**.
