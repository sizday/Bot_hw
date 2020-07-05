from preload.config import admin_id


class Admin:
    id = admin_id
    teachers = [admin_id]

    def add_teacher(self, teacher_id: int):
        self.teachers.append(teacher_id)

    def delete_teacher(self, teacher_id: int):
        self.teachers.remove(teacher_id)
