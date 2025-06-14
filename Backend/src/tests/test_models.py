from my_api.models import animal_prediction, new_animal
import pytest
from pydantic import ValidationError


def test_animal_prediction_valid():
    # Caso válido
    input_data = {
        "walks_on_n_legs": 4,
        "height": 1.2,
        "weight": 35.5,
        "has_wings": False,
        "has_tail": True
    }
    model = animal_prediction(**input_data)
    assert model.walks_on_n_legs == 4
    assert model.height == 1.2
    assert model.weight == 35.5
    assert not model.has_wings
    assert model.has_tail
    
    
def test_new_animal():
    # Caso válido
    input_data2 = {
        "walks_on_n_legs": 4,
        "height": 1.2,
        "weight": 35.5,
        "has_wings": False,
        "has_tail": True,
        "label": 2
    }
    model = new_animal(**input_data2) # the ** is used to unpack the dictionary into keyword arguments
    assert model.walks_on_n_legs == 4
    assert model.height == 1.2
    assert model.weight == 35.5
    assert not model.has_wings
    assert model.has_tail
    assert model.label == 2
    
    
def test_invalid_legs():
    # Invalid data_legs: 3
    with pytest.raises(ValidationError):
        animal_prediction(
            walks_on_n_legs=3,
            height=1.0,
            weight=10.0,
            has_wings=False,
            has_tail=True
        )