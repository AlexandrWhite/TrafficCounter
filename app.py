from flask import Flask, jsonify, Response, make_response, redirect, url_for, request, render_template
from video_processing import VideoPlayer
from datetime import datetime


app = Flask(__name__)
vp = VideoPlayer()

CSV_RESULT_PATH = '/dataset'

playlist = [
    ('video/test1.mp4','2024-01-05 17:57:41'),
    ('video/test2.mp4','2024-01-05 17:58:35')
    #('/content/drive/MyDrive/video1may3/930to1000.mp4','2024-01-05 09:32:09')
    # ('X:\\video_record\\1may\\900to930.mp4', '2024-01-05 09:00'),
    # ('X:\\video_record\\1may\\test1.mp4','2024-01-05 17:57:41'),
    # ('X:\\video_record\\1may\\test2.mp4','2024-01-05 17:58:34')
]



vp.set_playlist(playlist)
#vp.run_video(playlist[i][0], datetime.fromisoformat(playlist[i][1]))

vp.add_line(284,49, 617,253, 781,439)
vp.add_line(161,170, 369,424, 781,439)
vp.add_line(276,432, 607,212, 781,439)
vp.add_line(1,272, 454,34, 781,439)

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