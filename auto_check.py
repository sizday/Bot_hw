def open_file(file_name_answer, file_name_test):
    answer_file = open(file_name_answer, encoding='utf-8')
    answer = file_to_list(answer_file)
    answer_file.close()
    test_file = open(file_name_test, encoding='utf-8')
    test = file_to_list(test_file)
    test_file.close()
    compare_answer(answer, test)


def file_to_list(answer):
    answer_list = []
    for line in answer:
        if line.endswith('\n'):
            line = line[:-1]
        line = line[3:]
        answer_list.append(line)
    return answer_list


def compare_answer(answer_list, test_list):
    count = 0
    for i in range(len(answer_list)):
        if answer_list[i] == test_list[i]:
            count += 1
    result = round(count/len(answer_list)*100)
    return result


open_file('text_file/answer.txt', 'text_file/hw_test.txt')