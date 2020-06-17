import cv2


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


def compare_picture(my_file, original_file):
    hash1 = calc_image_hash(my_file)
    hash2 = calc_image_hash(original_file)
    percent = compare_hash(hash1, hash2)
    return percent
