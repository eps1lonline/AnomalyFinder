from operations.del_and_create_dir import del_and_create_dir
from operations.video_processing import video_processing
from operations.create_time_series import create_time_series
from operations.draw_graphic import draw_graphic
from operations.find_coef import find_coef

import time

def all_operations(progrBar_progressBar, window, anom_rBut_sel_value, coef_anom, video_path, output_path, h_line_pts, coef, speed):
    """Выполняет все операции по порядку"""
    
    # Время старта
    start_time = time.time()
 
    # 1
    dir = del_and_create_dir(output_path)

    # 2
    all_dist, all_time, speed_obj = video_processing(dir, progrBar_progressBar, window, video_path, h_line_pts, coef)

    # 3
    create_time_series(all_dist, all_time, dir, speed_obj, coef)
    
    # 4
    draw_graphic(speed_obj, anom_rBut_sel_value, coef_anom, dir)

    # 5
    if (coef == 1):
        find_coef(speed_obj, speed, video_path)

    # Время конца
    end_time = time.time()
    print(f"Время выполнения программы {end_time - start_time:.2f} секунд")
