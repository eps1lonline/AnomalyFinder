from ultralytics import YOLO, solutions
from tkinter import * 

import cv2
import os

def video_processing(dir, progrBar_progressBar, window, video_path, h_line_pts, coef):
    """Обработка видео"""

    cap = cv2.VideoCapture(video_path)
    
    # Проверка на сущесвование файла
    assert cap.isOpened(), "Ошибка чтения видеофайла"

    # Получение параметров видео
    w, h, fps = (int(cap.get(x)) for x in (
        cv2.CAP_PROP_FRAME_WIDTH, 
        cv2.CAP_PROP_FRAME_HEIGHT, 
        cv2.CAP_PROP_FPS
    ))

    # Кол-во кадров в видео
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) 

    # Инициализация видеописателя
    video_writer = cv2.VideoWriter(
        os.path.join(dir["final_video"], "final_video.avi"), 
        cv2.VideoWriter_fourcc(*"mp4v"), 
        fps, 
        (w, h)
    )

    # Задаём начальный статус для progress_bar
    progrBar_progressBar['value'] = 0
    window.update()

    # Загрузка модели
    model = YOLO("yolov8n.pt") 
    names = model.model.names  
    
    # Определение горизонтальной линии (розовая линия)
    line_pts = [(0, h_line_pts), (int(w), h_line_pts)]

    # Инициализация объекта оценки скорости
    speed_obj = solutions.SpeedEstimator(reg_pts=line_pts, names=names, view_img=True)

    # Переменные для сохранения скриншотов
    count = 0
    flag = False

    # Сохраняю каждую координату объекта и его время в каждый момент
    all_dist = {}
    all_time = {}

    # Прогресс программы
    progr = 1

    # Ядро скрипта обрабатывает видео кадр за кадром
    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            break

        # Отслеживание объектов и оценка скорости
        tracks = model.track(im0, persist=True, show=False, verbose=False)
        im0 = speed_obj.estimate_speed(im0, tracks, coef)
        video_writer.write(im0)

        # Создание скриншотов автомобилей при пересечении линии
        if len(speed_obj.trkd_ids) != count and flag:
            for i in range(count, len(speed_obj.trkd_ids)):
                cv2.imwrite(os.path.join(dir["screenshots"], f"screenshot_{speed_obj.trkd_ids[i]}.png"), im0)
                print(f"'screenshot_{speed_obj.trkd_ids[i]}.png' сохранён")
                count += 1
            flag = False

        if len(speed_obj.trkd_ids) != count:
            flag = True
        
        # Сбор данных о расстоянии
        for i in speed_obj.trk_history:
            if i not in all_dist:
                all_dist[i] = []
            length = len(speed_obj.trk_history[i]) - 1
            all_dist[i].append(speed_obj.trk_history[i][length])

        # Сбор данных о времени
        for i in speed_obj.trk_pt:
            if i not in all_time:
                all_time[i] = []
            all_time[i].append(speed_obj.trk_pt[i])

        # Вывод прогресса
        print(f'Progress: ({progr}/{frame_count})')
        percentage = (progr / frame_count) * 100
        progrBar_progressBar['value'] = percentage
        progrBar_label = Label(window, text=f"{progr}/{frame_count}")
        progrBar_label.place(x=340, y=550)
        window.update()

        progr += 1

    # Убирает повторы в словаре all_distance
    for i in all_dist:
        seen = set()
        all_dist[i] = [j for j in all_dist[i] if not (j in seen or seen.add(j))]

    # Убирает повторы в словаре all_time
    for i in all_time:
        seen = set()
        all_time[i] = [j for j in all_time[i] if not (j in seen or seen.add(j))]

    print(f"\nВидео обработано и сохранено '{dir['final_video']}'")

    return all_dist, all_time, speed_obj