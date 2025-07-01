from datetime import datetime
from fastapi import FastAPI
from monitor import MachineMetric

m = MachineMetric(config='mm/config.yaml')
app = FastAPI()

@app.get("/info")
async def info():
    return m.info

@app.get("/metrics")
async def metrics():
    res = m.metrics()
    res['timestamp'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")
    return res

