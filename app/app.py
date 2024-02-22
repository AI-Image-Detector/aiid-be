import os
import io
import torch
import time
from torchvision import models, transforms
from PIL import Image
from flask import Flask, request
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)

    except OSError:
        pass
    
    @app.route('/', methods=['GET'])
    def hello():
        return {"message":"Hello, if you get this message, it means this service is running."}
    
    @app.route('/predict', methods=['POST'])
    def predict():
        if request.method=='POST':
            if 'image' not in request.files:
                return {'error': 'No file part'}
            
            file = request.files['image']

            if file.filename == '':
                return {'error': 'No selected file'}
            
            image = read_file(file)
            tensor = to_tensor(image)

            time_start = time.time()
            predicted_class, probability = do_predict(tensor)
            time_end = time.time()

            return {'predicted_class':predicted_class,
                    'probability':probability,
                    'prediction_time':time_end-time_start}
        
    return app

def do_predict(tensor):
    classes = ['ai', 'nature']
    model = get_model()
    
    model.eval()
    outputs = model(tensor)
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    
    max_probability, _ = torch.max(probabilities, 0)
    predicted_index = torch.argmax(probabilities).item()
    predicted_class = classes[predicted_index]

    return predicted_class, max_probability.item()
        
def get_model():
    savedmodel_path = './model/model.pt'
    model = models.resnet50(pretrained=False)
    for param in model.parameters():
        param.requires_grad = True
    n_inputs = model.fc.in_features
    model.fc = torch.nn.Linear(n_inputs, 2)
    model.load_state_dict(torch.load(savedmodel_path, map_location='cpu'))
    return model

def read_file(file):
    try:
        image = Image.open(io.BytesIO(file.read()))
        return image
    except Exception as e:
        return {'error': 'Unable to read the image',
                'details': str(e)}
    
def to_tensor(image):
    transform = transforms.Compose([transforms.Resize(300),
                                    transforms.CenterCrop(299),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.485, 0.456, 0.406],
                                                        [0.229, 0.224, 0.225])])

    return transform(image).unsqueeze(0)