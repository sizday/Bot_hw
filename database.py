from aiogram import types
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import (Column, Integer, String, Sequence, Boolean)
from sqlalchemy import sql
from config import db_pass, db_user, host
import operator

db = Gino()


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(Integer)
    full_name = Column(String(100))
    username = Column(String(50))
    query: sql.Select


class HW(db.Model):
    __tablename__ = 'home_works'
    id = Column(Integer, Sequence('hw_id_seq'), primary_key=True)
    title = Column(String(50))
    description = Column(String(200))
    type = Column(String(200))
    file = Column(String(200))
    answer = Column(String(200), default='')
    query: sql.Select


class Done(db.Model):
    __tablename__ = 'done_hw'
    id = Column(Integer, Sequence('done_id_seq'), primary_key=True)
    student_id = Column(Integer)
    homework_id = Column(Integer)
    answer = Column(String(200))
    successful = Column(Boolean, default=False)
    marks = Column(Integer, default=-1)
    query: sql.Select


class DBCommands:

    async def get_user(self, user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def get_hw(self, homework_id) -> HW:
        homework = await HW.query.where(HW.id == homework_id).gino.first()
        return homework

    async def get_done(self, student_id, homework_id) -> Done:
        done = await Done.query.where(Done.student_id == student_id and Done.homework_id == homework_id).gino.first()
        return done

    async def check_hw(self, student_id, homework_id, parameter1, parameter2):
        hw = await self.get_hw(homework_id)
        hw_type = hw.type
        hw_type.check_hw(parameter1, parameter2)
        hw_type.set_marks()
        await self.rate_hw(student_id, homework_id, hw_type.mark)
        return hw_type.mark

    async def list_hw(self):
        hw = await HW.query.gino.all()
        return hw

    async def list_user(self):
        users = await User.query.gino.all()
        return users

    async def list_done(self):
        done = await Done.query.gino.all()
        return done

    async def count_users(self) -> int:
        total = await db.func.count(User.id).gino.scalar()
        return total

    async def count_hw(self) -> int:
        total = await db.func.count(HW.id).gino.scalar()
        return total

    async def exist_user(self) -> str:
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return 'old'
        return 'new'

    async def add_new_user(self) -> (User, str):
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return old_user, 'old'
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name
        await new_user.create()
        all_hw = await self.list_hw()
        for num, hw in enumerate(all_hw):
            new_done = Done()
            new_done.student_id = new_user.id
            new_done.homework_id = hw.id
            await new_done.create()
        return new_user, 'new'

    async def list_marks_by_id(self, user_id):
        all_done = await Done.query.where(Done.student_id == user_id).gino.all()
        list_marks = []
        for num, done in enumerate(all_done):
            list_marks.append(done.marks)
        return list_marks

    async def list_all_marks(self):
        users = await self.list_user()
        list_users = []
        list_marks = []
        for num, user in enumerate(users):
            list_users.append(user.id)
            current_user_marks = await self.list_marks_by_id(user.id)
            list_marks.append(round(sum(current_user_marks)/len(current_user_marks), 2))
        users_marks = dict.fromkeys(list_users, list_marks)
        # sorted_users_marks = sorted(users_marks.items(), key=operator.itemgetter(1))
        return users_marks

    async def rate_hw(self, user_id, hw_id, mark):
        current_done = await Done.query.where(Done.student_id == user_id and Done.homework_id == hw_id).gino.first()
        await current_done.update(marks=mark).apply()

    async def update_done(self, user_id, hw_id, answer):
        current_done = await Done.query.where(Done.student_id == user_id and Done.homework_id == hw_id).gino.first()
        await current_done.update(successful=True).apply()
        await current_done.update(answer=answer).apply()

    async def done_unmade(self):
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        done_unmade_list = await Done.query.where((Done.student_id == user.id) & (Done.successful == False)).gino.all()
        return done_unmade_list


async def create_db():
    await db.set_bind(f'postgresql://{db_user}:{db_pass}@{host}/gino')
    db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()
    await db.gino.create_all()
