import cv2
import io


def calc_image_hash(filename):
    image = cv2.imread(filename)
    resized = cv2.resize(image, (8, 8), interpolation=cv2.INTER_AREA)
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    avg = gray_image.mean()
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)

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


def compare_picture(original, test):
    original_file = io.BytesIO(original.read())
    test_file = io.BytesIO(test.read())
    hash1 = calc_image_hash(test_file)
    hash2 = calc_image_hash(original_file)
    percent = compare_hash(hash1, hash2)
    if percent < 20:
        mark = 5
    elif percent < 30:
        mark = 4
    elif percent < 40:
        mark = 3
    else:
        mark = 2
    return mark
