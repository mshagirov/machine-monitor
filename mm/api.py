from datetime import datetime

from fastapi import FastAPI

from monitor import MachineMetric

m = MachineMetric(config='mm/config.yaml')
app = FastAPI()

@app.get("/")
async def root():
    return m.info

@app.get("/metrics")
async def metrics():
    res = {'datetime':datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")}
    for key, val in m.metrics().items():
        res[key] = val
    return res

