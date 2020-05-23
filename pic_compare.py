import cv2
import difflib


# Функция вычисления хэша
def calc_image_hash(filename):
    image = cv2.imread(filename)  # Прочитаем картинку
    resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)  # Переведем в черно-белый формат
    avg = gray_image.mean()  # Среднее значение пикселя
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)  # Бинаризация по порогу

    # Рассчитаем хэш
    _hash = ""
    for x in range(8):
        for y in range(8):
            val = threshold_image[x, y]
            if val == 255:
                _hash = _hash + "1"
            else:
                _hash = _hash + "0"

    return _hash


def compare_hash(hash_1pic, hash_2pic):
    i = 0
    count = 0
    while i < len(hash_1pic):
        if hash_1pic[i] != hash_2pic[i]:
            count = count + 1
        i = i + 1
    return count


hash1 = calc_image_hash("img/original.png")
hash2 = calc_image_hash("img/logo.jpg")
print(hash1)
print(hash2)
print(compare_hash(hash1, hash2))