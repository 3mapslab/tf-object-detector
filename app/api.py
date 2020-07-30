import object_detection_api
import os
from PIL import Image
from flask import Flask, request, Response
import json
from datetime import datetime

#import logging
#log = logging.getLogger('werkzeug')
#log.setLevel(logging.ERROR)

app = Flask(__name__)

# for CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST') # Put any other methods you need here
    return response


@app.route('/', methods=['GET'])
def index():
    return Response(response=json.dumps({
        "about": "tf-object-detector v1.0.0",
        "now": datetime.now(),
        "tensorflow_version": object_detection_api.tf.__version__,
        "tensorflow_model": os.environ['TENSORFLOW_MODEL']
    }, indent=4, sort_keys=True, default=str),
        status=200,mimetype="application/json")

@app.route('/image', methods=['POST'])
def image():
    try:
        image_file = request.files['image']  # get the image

        # Set an image confidence threshold value to limit returned data
        threshold = request.form.get('threshold')
        if threshold is None:
            threshold = 0.5
        else:
            threshold = float(threshold)

        # Get the target object class to be detected (alternative: request.headers['target_class'])
        target_class = request.form.get('target_class')

        return Response(response=json.dumps({'Target class':target_class},indent=4, sort_keys=True, default=str),status=200,mimetype="application/json")

        # finally run the image through tensor flow object detection
        image_object = Image.open(image_file)
        objects = object_detection_api.get_objects(image_object, target_class, threshold)

        json_output = json.dumps(objects,indent=4, sort_keys=True, default=str)

        response = Response(response=json_output,status=200,mimetype="application/json")
        return response
    except Exception as e:
        return Response(response=json.dumps({'error':e},indent=4, sort_keys=True, default=str),status=500,mimetype="application/json")