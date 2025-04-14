def find_coef(speed_obj, speed, video_path):
    sum = 0
    for i in speed_obj.spd:
        sum += speed_obj.spd[i]

    coef = (speed * len(speed_obj.spd)) / sum

    print(f"Значение coef={coef}")