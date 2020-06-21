from spellchecker import SpellChecker
import string

spell = SpellChecker()


def unit_clear_line(line_clear):
    file_text = ""
    for i in range(len(line_clear)):
        file_text += line_clear[i]
    file_text = file_text.lower().split()
    return file_text


def clear_me(file_text):
    stop_list = string.punctuation + string.digits + '«»·—'
    stop_list = stop_list.replace('-', '')
    line_clear = [i for i in file_text if (i not in stop_list)]
    return unit_clear_line(line_clear)


def check_text(answer_file):
    answer_text = str(answer_file.getvalue(), 'utf-8')
    text = clear_me(answer_text)
    print(text)
    misspelled = spell.unknown(text)
    return len(misspelled)
