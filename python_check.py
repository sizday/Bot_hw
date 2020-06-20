import subprocess
import os


def compare_files(answer_file, program_file):
    answer_text = str(answer_file.getvalue(), 'utf-8')
    temp_origin = "my_program.py"
    with open(temp_origin, 'wb') as original_file:
        original_file.write(program_file.read())
    program = "python my_program.py"
    process = subprocess.Popen(program, stdout=subprocess.PIPE, encoding='utf-8')
    data_text = process.communicate()[0]
    os.remove(temp_origin)
    if answer_text == data_text:
        return 5
    else:
        return 2
