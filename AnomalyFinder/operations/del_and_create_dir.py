import shutil
import os

def del_and_create_dir(output_path):
    """Удаляет старые и создаёт новые директории"""

    # Словарь папок, которые будем создавать
    directories = { 
        "graphic":              os.path.join(output_path, "graphic"),
        "final_video":          os.path.join(output_path, "final_video"),
        "time_series":          os.path.join(output_path, "time_series"),
        "screenshots":          os.path.join(output_path, "screenshots"),
        "screenshots_anomaly":  os.path.join(output_path, "screenshots_anomaly")
    }
    
    def delete_directory(dir):
        """Удаляет директории"""

        if os.path.exists(dir) and os.path.isdir(dir):
            shutil.rmtree(dir)
            print(f"Папка '{dir}' удалена")
        else:
            print(f"Папка '{dir}' не найдена")

    # Удаляем диркетории
    for dir in directories.values():
        delete_directory(dir)
    print()

    def create_directory(dir):
        """Создает директорию"""

        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f"Папка '{dir}' создана")
        else:
            print(f"Папка '{dir}' не найдена")

    # Создаём директории
    for dir in directories.values():
        create_directory(dir)
    print()

    return directories