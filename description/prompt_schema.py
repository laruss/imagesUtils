"""
Consider to change the schema if you need gpt to create a JSON object in response.
"""
from pydantic import BaseModel, conlist


class Parameters(BaseModel):
    sports: float
    art: float
    music: float
    cinema: float
    literature: float
    technologies: float
    travel: float
    fashion: float
    foodAndDrink: float
    natureAndAnimals: float
    cars: float
    videoGames: float
    news: float
    eroticism: float


class GPTResponseJSON(BaseModel):
    parameters: Parameters
    descriptions: conlist(str, min_length=5, max_length=5)
