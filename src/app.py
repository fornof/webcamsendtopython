
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import io
import cv2
import base64
from PIL import Image
import imutils
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@socketio.on('image')
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)
    file = b.read()
    # Process the image frame
    #frame = pimg.read()
    #frame = imutils.resize(frame, width=700)
    #frame = cv2.flip(frame, 1)
    #imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(file).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)