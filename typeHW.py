from auto_check import open_file
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



class PictureHW(TypeHW):
    name = 'Picture'

    def check_hw(self, my_picture, original_picture):
        self.percent = compare_picture(my_picture, original_picture)
