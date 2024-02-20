import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from inference import get_flower_name, get_probability

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
        if request.method=='POST':
            file=request.files['file']
            image=file.read()
            flower_name=get_flower_name(image_bytes=image)
            probabilities=get_probability(image_bytes=image)
            # return render_template('result.html',flower=flower_name,prob=probabilities)

    return app