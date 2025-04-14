import math
import os

def create_time_series(all_dist, all_time, dir, speed_obj, coef):
    """Создаёт временной ряд"""

    # Запись временного ряда в файл
    with open(os.path.join(dir["time_series"], "time_series.txt"), 'w') as file:
        file.write(f'{"id":<10} {"coordinates(x;y)":<50} {"time(s)":<25} {"distance(px)":<25} {"speed(km/h)":<25}\n')
        
        for i in speed_obj.trkd_ids:
            d = 0
        
            for j in range(len(all_dist[i])):
                # Расстояние
                if j != 0:
                    x1 = all_dist[i][j - 1][0]
                    y1 = all_dist[i][j - 1][1]
                    x2 = all_dist[i][j][0]
                    y2 = all_dist[i][j][1]
                    d += math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

                # Время
                t = all_time[i][j] - all_time[i][0]

                # Скорость
                u = speed_obj.spd[i] * coef

                # Вывод
                x, y = all_dist[i][j]
                file.write(f'{i:<10} {f"({x},{y})":<50} {t:<25} {(d):<25} {(u):<25}\n')
            file.write('\n')

    print(f"Временной ряд сформирован и сохранён '{dir['time_series']}'")
