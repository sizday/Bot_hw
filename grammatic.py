from enchant import Dict
import string


def unit_clear_line(line_clear):
    file_text = ""
    for i in range(len(line_clear)):
        file_text += line_clear[i]
    return file_text


def clear_me(file_text):
    stop_list = string.punctuation + string.digits + '«»·'
    stop_list = stop_list.replace('-', '')
    line_clear = [i for i in file_text if (i not in stop_list)]
    return unit_clear_line(line_clear)


def check_text(answer_file, language):
    answer_text = str(answer_file.getvalue(), 'utf-8')
    text = clear_me(answer_text)
    list_text = text.replace('\n', ' ').split(' ')
    if language == 'ru_RU':
        stop_word = ['', '—', '--', '-го']
    else:
        stop_word = ['', '—', 'th', 's']
    d = Dict(language)
    mistakes = 0
    for word in list_text:
        if word not in stop_word:
            if not d.check(word):
                mistakes += 1
                # print(word)
                # print(d.suggest(word))
    return mistakes


# check_text('text_en.txt', 'en_EN')
# check_text('text_file/text_ru.txt', 'ru_RU')