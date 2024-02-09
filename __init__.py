import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins=["http://localhost:5173"])

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

    # a simple page that says hello
    @app.route('/', methods=['GET'])
    def hello():
        return {"message":"Hello, if you get this message, it means this service is running."}
    
    # predict endpoint
    @app.route('/predict', methods=['POST'])
    def predict():
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     return {"error": "No file part in the request"}

        # # check file extensions
        # def allowed_file(filename):
        #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}
        
        # file = request.files['file']
        # if file.filename == '':
        #     return {"error": "No file selected"}
        # if not allowed_file(file.filename):
        #     return {"error": "Invalid file extension"}
        
        # # read the image file
        # image = Image.open(file)

        # preprocess the image
    
        # make prediction

        # return the prediction

        if request.method == 'POST':
            data = request.get_json()
            return {"prediction": data.get('image')}
        else:
            return {"message":"This is a prediction endpoint."}

    return app