from flask import Flask, jsonify, Response, make_response, redirect, url_for, request, render_template
from video_processing import VideoPlayer

app = Flask(__name__)
vp = VideoPlayer()

vp.run_video('/content/MyDrive/test1.mp4')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video', methods=['GET','POST'])
def video():
    new_frame = vp.generate_frames()
    return Response(new_frame,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)