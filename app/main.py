from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.templating import Jinja2Templates
from prometheus_client import Counter, generate_latest
import socket
import datetime
import psutil

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total App Requests"
)

@app.get("/")
def home(request: Request):
    REQUEST_COUNT.inc()

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    uptime = datetime.datetime.now().strftime("%H:%M:%S")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "hostname": socket.gethostname(),
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Healthy",
            "cpu": cpu_usage,
            "memory": memory_usage,
            "uptime": uptime
        }
    )

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )