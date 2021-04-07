from flask import Flask, send_from_directory, abort
app = Flask(__name__)

@app.route('/images/<string:image_name>')
def hello_world(image_name):
    return image_name
    #testgit