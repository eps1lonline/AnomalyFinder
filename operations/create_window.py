from operations.all_operations import all_operations

from tkinter import filedialog
from tkinter import ttk
from tkinter import * 

import cv2

def create_window():
    """Создаёт mainFrame"""
    
    window = Tk()
    window.title("AnomalyFinder")
    window.geometry("410x590")

    # 1
    video_path_label = Label(window, text="1. Путь к видеофайлу:")
    video_path_label.place(x=20, y=20)

    video_path_entry = Entry(window, width=50)
    video_path_entry.insert(END, "C:/Users/nikit/Desktop/Git Uploads/AnomalyFinder/data_set/car.mp4")
    video_path_entry.place(x=20, y=50)
    
    def video_path_but_funct():
        """Указываем путь к обрабатываемому видео"""

        video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        video_path_entry.delete(0, END)
        video_path_entry.insert(0, video_path)

    video_path_but = Button(window, text="Обзор", command=video_path_but_funct)
    video_path_but.place(x=340, y=45)

    # 2
    output_path_label = Label(window, text="2. Путь для сохранения результатов:")
    output_path_label.place(x=20, y=80)

    output_path_entry = Entry(window, width=50)
    output_path_entry.insert(END, "C:/Users/nikit/Desktop")
    output_path_entry.place(x=20, y=110)

    def output_path_but_funct():
        """Указываем путь для сохранения результатов"""

        output_path = filedialog.askdirectory()
        output_path_entry.delete(0, END)
        output_path_entry.insert(0, output_path)

    output_path_but = Button(window, text="Обзор", command=output_path_but_funct)
    output_path_but.place(x=340, y=105)

    # 3
    anom_label = Label(window, text="3. Условие для нахождения аномалий:")
    anom_label.place(x=20, y=140)

    anom_rBut_sel_value = IntVar()
    anom_rBut_sel_value.set(4)

    anom_max_rBut = Radiobutton(window, text="Max", variable=anom_rBut_sel_value, value=1)
    anom_max_rBut.place(x=20, y=170)

    anom_min_rBut = Radiobutton(window, text="Min", variable=anom_rBut_sel_value, value=2)
    anom_min_rBut.place(x=20, y=200)

    anom_max_min_rBut = Radiobutton(window, text="Max/Min", variable=anom_rBut_sel_value, value=3)
    anom_max_min_rBut.place(x=110, y=170)

    anom_avrg_rBut = Radiobutton(window, text="Avrg", variable=anom_rBut_sel_value, value=4)
    anom_avrg_rBut.place(x=110, y=200)

    anom_text = Text(window, height=1, width=5)
    anom_text.insert(END, 20)
    anom_text.place(x=175, y=200)

    anom_km_h_label = Label(window, text="km/h")
    anom_km_h_label.place(x=220, y=200)

    def anom_info_but_funct():
        """Создаёт окно с дополнительной информацией"""

        anom_window_info = Tk()
        anom_window_info.title("Information")
        anom_window_info.geometry("800x250")

        msg = (
            "Max:\n"
            "Аномалия — это максимальное значение, а также значения, которые составляют не менее 80% от этого максимума.\n"
            "Например: если 100 км/ч — это максимальное значение, то всё, что больше 80 км/ч, считается аномалией.\n\n"

            "Min:\n"
            "Аномалия - это минимальное значение, а также значения, которые составляют не более 120% от этого минимума.\n"
            "Например: если 100 км/ч — это минимальное значение, то всё, что меньше 120 км/ч, считается аномалией.\n\n"

            "Max/Min:\n"
            "Совокупность Min и Max.\n\n"

            "Avrg:\n"
            "Аномалия - это значения, которые превышают среднее значение на N.\n"
            "Например: если 100 км/ч - это среднее значение, то всё, что больше 100 + N (км/ч) или меньше 100 - N (км/ч), считается аномалией.\n"
        )

        anom_window_info_label = Label(anom_window_info, text=msg)
        anom_window_info_label.place(x=20, y=20)

    anom_info_but = Button(window, text="Information", command=anom_info_but_funct)
    anom_info_but.place(x=20, y=235)

    # 4
    coef_label = Label(window, text="4. Вычисление коэффициента для расчёта скорости:")
    coef_label.place(x=20, y=275)

    coef_center_label = Label(window, text="Center")
    coef_center_label.place(x=20, y=305)

    coef_center_text = Text(window, height=1, width=6)
    coef_center_text.insert(END, 415)
    coef_center_text.place(x=85, y=305)

    coef_center_px_label = Label(window, text="px")
    coef_center_px_label.place(x=140, y=305)

    def click_event(event, x, y, flags, param):
        """Функция для обработки клика мыши"""

        if event == cv2.EVENT_LBUTTONDOWN:  # Проверяем, было ли нажатие левой кнопкой мыши
            coef_center_text.delete("1.0", END)
            coef_center_text.insert(END, y)
            cv2.destroyAllWindows()  # Закрываем окно при нажатии

    def coef_center_but_funct():
        """Указываем на фотографии центр пути"""

        cap = cv2.VideoCapture(video_path_entry.get())
        
        if not cap.isOpened():
            print("Ошибка чтения видеофайла")
        else:
            ret, frame = cap.read() # Читаем первый кадр
            if ret:
                cv2.imshow("Center", frame) # Показывает первый кадр
                cv2.setMouseCallback("Center", click_event)
                cv2.waitKey(0)  # Ожидаем нажатия клавиши
            else:
                print("Ошибка чтения видеофайла")

        # Освобождаем ресурсы
        cap.release()
        cv2.destroyAllWindows()

    coef_center_but = Button(window, text="Указать", command=coef_center_but_funct)
    coef_center_but.place(x=185, y=300)

    coef_speed_label = Label(window, text="Speed")
    coef_speed_label.place(x=20, y=335)

    coef_speed_text = Text(window, height=1, width=6)
    coef_speed_text.insert(END, 90)
    coef_speed_text.place(x=85, y=335)

    coef_speed_km_h_label = Label(window, text="km/h")
    coef_speed_km_h_label.place(x=140, y=335)

    coef_coef_label = Label(window, text="Coef")
    coef_coef_label.place(x=20, y=365)

    coef_coef_text = Text(window, height=1, width=6)
    coef_coef_text.insert(END, 1)
    coef_coef_text.place(x=85, y=365)

    def coef_info_but_funct():
        """Создаёт окно с дополнительной информацией"""

        coef_window_info = Tk()
        coef_window_info.title("Information")
        coef_window_info.geometry("730x240")

        msg = (
            "Center:\n"
            "Пользователь указывает на центр пути. Скорость будет показываться, когда объект пересечёт эту линию.\n"
            "Начало пути — момент, когда камера впервые начинает отслеживать объект.\n"
            "Конец пути — момент, когда камера прекращает отслеживание.\n\n"

            "Speed:\n"
            "Дополнительный параматр для вычисления коэффициента.\n"
            "Например, если скорость ограничена знаком, то Speed равно этому ограничению.\n\n"

            "Coef:\n"
            "Для подсчёта скорости.\n"
            "Программа запускается с начальным значением 1 и в конце выдаст коэффициент для корректного отображения скорости.\n"
            "Необходимо повторно запустить программу с новым коэффициентом.\n\n"
        )

        coef_window_info_label = Label(coef_window_info, text=msg)
        coef_window_info_label.place(x=20, y=20)

    coef_info_but = Button(window, text="Information", command=coef_info_but_funct)
    coef_info_but.place(x=20, y=400)

    # 5
    start_label = Label(window, text="5. Запуск программы:")
    start_label.place(x=20, y=440)

    def start_but_funct():
        """Запускает программу"""

        video_path = video_path_entry.get()
        output_path = output_path_entry.get()
        coef_anom = float(anom_text.get("1.0", END))
        h_line_pts = int(coef_center_text.get("1.0", END))

        # car = 90 km/h
        # people = 4.5 km/h
        speed = float(coef_speed_text.get("1.0", END))

        # car = 3.3462711120278352
        # people = 0.2723344582573448
        coef = float(coef_coef_text.get("1.0", END))

        all_operations(progrBar_progressBar, window, anom_rBut_sel_value, coef_anom, video_path, output_path, h_line_pts, coef, speed)

    start_but = Button(window, text="Start", height=2, width=9, command=start_but_funct)
    start_but.place(x=20, y=470)

    # 6
    progrBar_lable = Label(window, text="Прогресс выполнения:")
    progrBar_lable.place(x=20, y=520)

    progrBar_progressBar = ttk.Progressbar(window, orient=HORIZONTAL, length=305, mode='determinate', style="custom.Horizontal.TProgressbar")
    progrBar_progressBar.place(x=20, y=550)

    window.mainloop()
