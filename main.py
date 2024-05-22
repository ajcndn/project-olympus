from fastapi import FastAPI
from olympus import Olympus
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

app.mount("/", StaticFiles(directory="UI", html=True), name="static")

class Item(BaseModel):
    idea: str

@app.post("/run_olympus")
def run_olympus(item: Item):
    olympus = Olympus()
    olympus.get_user_input(product_idea)
    olympus.instantiate_agents()
    olympus.instantiate_tasks()
    olympus.form_crew_and_kickoff()
    results = olympus.results
    return {"results": results}
