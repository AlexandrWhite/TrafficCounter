from video_processing import VideoPlayer

vp = VideoPlayer()
playlist = [
    #('video/test1.mp4', '2024-01-05 06:29:47'),
    #('video/test2.mp4', '2024-01-05 06:29:47')
    #('video/test2.mp4', '2024-01-05 06:29:47')
    # #('/content/drive/MyDrive/video1may3/630to7.mp4','2024-01-05 06:29:47'),
    # #('/content/drive/MyDrive/video1may3/700to730.mp4','2024-01-05 06:57:30'),
    # #('/content/drive/MyDrive/video1may3/730to800.mp4','2024-01-05 07:33:30'),
    # #('/content/drive/MyDrive/video1may3/800to830.mp4','2024-01-05 07:55:20'),
    ('/content/drive/MyDrive/video1may3/830to900.mp4','2024-01-05 08:33:35'),
    ('/content/drive/MyDrive/video1may3/900to930.mp4','2024-01-05 09:01:08'),
    ('/content/drive/MyDrive/video1may3/930to1000.mp4','2024-01-05 09:32:08'),
    ('/content/drive/MyDrive/video1may3/1000to1030.mp4','2024-01-05 10:05:48'),
    ('/content/drive/MyDrive/video1may3/1030to1100.mp4','2024-01-05 10:32:10'),
    ('/content/drive/MyDrive/video1may3/1100to1130.mp4','2024-01-05 10:58:47'),
    
    #не грузил
    ('/content/drive/MyDrive/video1may3/1130to1200.mp4','2024-01-05 11:29:14'),

    ('/content/drive/MyDrive/video1may3/1200to1230.mp4','2024-01-05 11:56:01'),
    ('/content/drive/MyDrive/video1may3/1230to1300.mp4','2024-01-05 12:26:05'),
    ('/content/drive/MyDrive/video1may3/1300to1330.mp4','2024-01-05 13:04:03'),
    ('/content/drive/MyDrive/video1may3/1330to1400.mp4','2024-01-05 13:29:54'),
    ('/content/drive/MyDrive/video1may3/1400to1430.mp4','2024-01-05 14:03:45'),
    ('/content/drive/MyDrive/video1may3/1430to1500.mp4','2024-01-05 14:39:22'),
    ('/content/drive/MyDrive/video1may3/1500to1530.mp4','2024-01-05 15:04:08'),
    ('/content/drive/MyDrive/video1may3/1530to1600.mp4','2024-01-05 15:32:48'),
    ('/content/drive/MyDrive/video1may3/1600to1630.mp4','2024-01-05 16:01:49'),
    ('/content/drive/MyDrive/video1may3/1630to1700.mp4','2024-01-05 16:32:12'),
    ('/content/drive/MyDrive/video1may3/1700to1730.mp4','2024-01-05 17:04:31'),
    ('/content/drive/MyDrive/video1may3/1730to1800.mp4','2024-01-05 17:32:31')
]   



vp.set_playlist(playlist)


vp.add_line(284,49, 617,253, 781,439)
vp.add_line(161,170, 369,424, 781,439)
vp.add_line(276,432, 607,212, 781,439)
vp.add_line(1,272, 454,34, 781,439)

vp.generate_frames()