import json
import os

from dotenv import dotenv_values
from flask import Flask, render_template, Response, redirect, url_for
from flask_restful import Api, Resource
from flask_vite import Vite
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput

from modules.Camera import Camera
from modules.OCRSpace import OCR, overlay_image

config = dotenv_values(".env")
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
api = Api(app)
vite = Vite(app)
ocr = OCR(config.get('OCR_SPACE_API_KEY'))

if config.get('APP_DEBUG') == 'False':
    encoder = H264Encoder()
    output = CircularOutput()
    camera = Camera(encoder, output)


def gen_frames():
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# defines the route that will access the video feed and call the feed function
class VideoFeed(Resource):
    def get(self):
        return Response(gen_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    return render_template('index.j2')


@app.route('/scan')
def scan():
    fp = camera.video_snap()
    return redirect(url_for('search', filename=fp))


@app.route('/files')
def files():
    pic_dir = '{0}/pictures/'.format(app.static_folder)
    images = [f for f in os.listdir(pic_dir) if f.endswith(('.jpg', '.png'))]
    return render_template('files.j2', images=images)


@app.route('/scan/<filename>')
def search(filename):
    pic_dir = '{0}/pictures/'.format(app.static_folder)
    result_dir = '{0}/results/'.format(app.static_folder)
    json_filepath = os.path.join(result_dir, os.path.splitext(filename)[0] + '.json')

    if filename in os.listdir(pic_dir):
        if not os.path.exists(json_filepath):
            result = ocr.space_file(pic_dir + filename, overlay=True)
            with open(json_filepath, 'w') as json_file:
                json.dump(result, json_file)

        with open(json_filepath, 'r') as json_file:
            data = json.load(json_file)
        return overlay_image(filename, data, pictures_dir=pic_dir, output_dir="{0}/overlays/".format(app.static_folder))
    else:
        return "File not found", 404


api.add_resource(VideoFeed, '/cam')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
