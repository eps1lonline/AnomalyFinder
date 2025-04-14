import matplotlib.pyplot as plt

import shutil
import os

MAX_SPEED_COEF = 0.8
MIN_SPEED_COEF = 1.2

def horizontal_lines(anom_rButton_val, speed_list, max_x, coef_anom, max_y, min_y):
    """Рисует горизонтальные линии"""

    if anom_rButton_val.get() == 1:
        plt.plot([-1, max_x + 1], [max_y, max_y], color='green', linestyle='--') 
        plt.plot([-1, max_x + 1], [max_y * MAX_SPEED_COEF, max_y * MAX_SPEED_COEF], color='red', linestyle='--')
        plt.legend(['V max', f'V max * {MAX_SPEED_COEF}'], loc=2)
    elif anom_rButton_val.get() == 2:
        plt.plot([-1, max_x + 1], [min_y, min_y], color='green', linestyle='--')
        plt.plot([-1, max_x + 1], [min_y * MIN_SPEED_COEF, min_y * MIN_SPEED_COEF], color='red', linestyle='--')
        plt.legend(['V min', f'V min * {MIN_SPEED_COEF}'], loc=2)
    elif anom_rButton_val.get() == 3:
        plt.plot([-1, max_x + 1], [max_y, max_y], color='green', linestyle='--') 
        plt.plot([-1, max_x + 1], [max_y * MAX_SPEED_COEF, max_y * MAX_SPEED_COEF], color='red', linestyle='--')

        plt.plot([-1, max_x + 1], [min_y, min_y], color='yellow', linestyle='--')
        plt.plot([-1, max_x + 1], [min_y * MIN_SPEED_COEF, min_y * MIN_SPEED_COEF], color='orange', linestyle='--')
        plt.legend(['V max', f'V max * {MAX_SPEED_COEF}', 'V min', f'V min * {MIN_SPEED_COEF}'], loc=2)
    elif anom_rButton_val.get() == 4:
        avrg_sp = sum(speed_list) / len(speed_list)
        plt.plot([-1, max_x + 1], [avrg_sp, avrg_sp], color='green', linestyle='--') 
        plt.plot([-1, max_x + 1], [avrg_sp - coef_anom, avrg_sp - coef_anom], color='red', linestyle='--')
        plt.plot([-1, max_x + 1], [avrg_sp + coef_anom, avrg_sp + coef_anom], color='orange', linestyle='--')
        plt.legend(['V ср', f'V ср - {coef_anom}', f'V ср + {coef_anom}'], loc=2)

def draw_graphic(speed_obj, anom_rButton_val, coef_anom, dir):
    """Рисует график аномалий"""

    speed_list = list(speed_obj.spd.values())
    max_x = max(speed_obj.trkd_ids)
    max_y = max(speed_list)
    min_y = min(speed_list)

    plt.figure(figsize=(16, 9))
    plt.title('График скоростей', fontsize=20, fontname='Times New Roman')
    plt.axis([-1, max_x + 1, 0, max_y + (coef_anom + 2)])
    plt.xticks(speed_obj.trkd_ids) # На оси Х только точки из trkd_ids

    plt.xlabel('№ объекта', color='gray')
    plt.ylabel('Скорость', color='gray')
    plt.grid(True) # Сетка

    horizontal_lines(anom_rButton_val, speed_list, max_x, coef_anom, max_y, min_y)

    for i in speed_obj.trkd_ids:
        speed = speed_obj.spd[i]
        choice = anom_rButton_val.get()
        is_anomaly = False

        if choice == 1:
            if speed >= max_y * MAX_SPEED_COEF:
                is_anomaly = True
        elif choice == 2:
            if speed <= min_y * MIN_SPEED_COEF:
                is_anomaly = True
        elif choice == 3:
            if speed >= max_y * MAX_SPEED_COEF or speed <= min_y * MIN_SPEED_COEF:
                is_anomaly = True
        elif choice == 4:
            avrg_sp = sum(speed_list) / len(speed_list)
            if speed <= avrg_sp - coef_anom or speed >= avrg_sp + coef_anom:
                is_anomaly = True

        color = 'red' if is_anomaly else 'green'
        plt.plot([i], [speed], color=color, marker='D')
        plt.plot([i, i], [0, speed], color='black')
        if is_anomaly:
            plt.text(i, speed, 'Аномалия')
            shutil.copy(os.path.join(dir["screenshots"], f"screenshot_{i}.png"), dir["screenshots_anomaly"]) # Сохраняем скриншот аномалии
    
    plt.savefig(os.path.join(dir["graphic"], "graphic.png")) # Сохранение графика
    plt.show()

    print(f"График аномальных явлений построен и сохранён '{dir['graphic']}'")
    