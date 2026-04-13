from flask import Flask, render_template, Response, jsonify
from face_detection import generate_frames, detection_state

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/status')
def status():
    return jsonify(detection_state)

if __name__ == '__main__':
    app.run(debug=True)