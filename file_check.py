import os
import time
import hashlib
import fsevents

# Директория за наблюдение
directory_to_watch = "/Users/YourUsername/Documents"

# Функция за изчисляване на хеш стойност на файл
def file_hash(file_path):
    hash_object = hashlib.sha256()
    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            hash_object.update(chunk)
    return hash_object.hexdigest()

# Дикт с хеш стойности на оригиналните файлове
file_hashes = {}

# Функция за наблюдение на файловете
def monitor_files(event):
    global file_hashes
    for dirpath, dirnames, filenames in os.walk(directory_to_watch):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            current_hash = file_hash(file_path)
            if file_path not in file_hashes:
                file_hashes[file_path] = current_hash
            elif file_hashes[file_path] != current_hash:
                print(f"Warning: File {file_path} has been modified or encrypted!")
                # Можеш да добавиш възстановяване или аларми

if __name__ == "__main__":
    # Наблюдаване на промени в директорията
    observer = fsevents.Observer()
    observer.schedule(fsevents.Handler(monitor_files), directory_to_watch, file_events=True)
    observer.start()

    try:
        while True:
            time.sleep(10)  # Интервал на проверка
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
