from fastapi import FastAPI

from monitor import MachineMetric

m = MachineMetric(config='mm/config.yaml')
app = FastAPI()

@app.get("/")
async def root():
    return m.info

