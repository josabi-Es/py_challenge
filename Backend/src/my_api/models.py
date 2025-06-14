from pydantic import BaseModel
from typing import Literal 

class animal_prediction(BaseModel):
    walks_on_n_legs: Literal[2, 4]
    height: float
    weight: float
    has_wings: bool
    has_tail: bool
    
    
class new_animal(BaseModel):
    walks_on_n_legs: Literal[2, 4]
    height: float
    weight: float
    has_wings: bool
    has_tail: bool
    label: Literal[1,2,3,4]
    
