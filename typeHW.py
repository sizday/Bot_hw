from auto_check import open_file
from grammatic import check_text
from pic_compare import compare_picture
    
    
class TypeHW:
    name = 'Default'
    percent = 0
    mark = 0

    def check_hw(self, parameter1, parameter2):
        self.percent = 0    
    
    def set_mark(self):
        self.mark = 0


class TestHW(TypeHW):
    name = 'Test'
    
    def check_hw(self, my_file, answer_file):
        self.percent = open_file(my_file, answer_file)
    
    def set_mark(self):
        self.mark = self.percent / 20 + 1


class GrammarHW(TypeHW):
    name = 'Grammar'

    def check_hw(self, my_file, language):
        self.percent = check_text(my_file, language)
    
    def set_mark(self):
        if self.percent > 12:
            self.mark = 1
        else:
            self.mark = 5 - self.percent / 3


class PictureHW(TypeHW):
    name = 'Picture'

    def check_hw(self, my_picture, original_picture):
        self.percent = compare_picture(my_picture, original_picture)
