"""
Consider to change the schema if you need gpt to create a JSON object in response.
"""
from pydantic import BaseModel, conlist, Field


def float_field():
    return Field(float, ge=0, le=1)


class Parameters(BaseModel):
    sports: float = float_field()
    art: float = float_field()
    music: float = float_field()
    cinema: float = float_field()
    literature: float = float_field()
    technologies: float = float_field()
    travel: float = float_field()
    fashion: float = float_field()
    foodAndDrink: float = float_field()
    natureAndAnimals: float = float_field()
    cars: float = float_field()
    videoGames: float = float_field()
    news: float = float_field()
    eroticism: float = float_field()


class GPTResponseJSON(BaseModel):
    parameters: Parameters
    descriptions: conlist(str, min_length=5, max_length=5)
