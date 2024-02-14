import json
import torch
from commons import get_model,get_tensor
classes = ['ai', 'nature']
model=get_model()
def get_flower_name(image_bytes):
    tensor=get_tensor(image_bytes)
    model.eval()
    outputs=model(tensor)
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    predicted_index = torch.argmax(probabilities).item()
    predicted_class = classes[predicted_index]
    return predicted_class

def get_probability(image_bytes):
    tensor = get_tensor(image_bytes)
    model.eval()
    outputs = model(tensor)
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    max_probability, _ = torch.max(probabilities, 0)
    probability_percent = max_probability.item() * 100
    probability_percent_formatted = "{:.3f}%".format(probability_percent)
    return probability_percent_formatted

