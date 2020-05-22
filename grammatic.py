import enchant
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


def check_text(filename, language):
    text = open(filename, encoding='utf-8').read()
    # print(text)
    text = clear_me(text)
    list_text = text.replace('\n', ' ').split(' ')
    # print(list_text)
    if language == 'ru_RU':
        stop_word = ['', '—', '--', '-го']
    else:
        stop_word = ['', '—', 'th', 's']
    d = enchant.Dict(language)
    mistakes = 0
    for word in list_text:
        if word not in stop_word:
            if not d.check(word):
                mistakes += 1
                print(word)
                print(d.suggest(word))
    print(mistakes)
    '''
    print(d.check("short-story"))
    print(d.check("shortstory"))
    print(d.suggest("Yevgeny"))
    '''


# check_text('text_en.txt', 'en_EN')
check_text('text_file/text_ru.txt', 'ru_RU')
