from dotenv import dotenv_values
from flask import Flask, render_template, Response
from flask_restful import Api, Resource
from flask_vite import Vite
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput

from modules.Camera import Camera

config = dotenv_values(".env")
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')
api = Api(app)
vite = Vite(app)

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
    fo = camera.video_snap()
    print(fo)
    return render_template('scan.j2', snippet=fo)


api.add_resource(VideoFeed, '/cam')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
