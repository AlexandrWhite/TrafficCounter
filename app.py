from flask import Flask, jsonify, Response, make_response, redirect, url_for, request, render_template
from video_processing import VideoPlayer
from datetime import datetime


app = Flask(__name__)
vp = VideoPlayer()

playlist = [
    ('test1.mp4','2024-01-05 17:57:41')
    #('/content/drive/MyDrive/video1may3/930to1000.mp4','2024-01-05 09:32:09')
    # ('X:\\video_record\\1may\\900to930.mp4', '2024-01-05 09:00'),
    # ('X:\\video_record\\1may\\test1.mp4','2024-01-05 17:57:41'),
    # ('X:\\video_record\\1may\\test2.mp4','2024-01-05 17:58:34')
]

i = 0

vp.run_video(playlist[i][0], datetime.fromisoformat(playlist[i][1]))

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