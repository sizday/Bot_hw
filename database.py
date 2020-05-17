from aiogram import types
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import (Column, Integer, BigInteger, String, Sequence, Boolean)
from sqlalchemy import sql

from config import db_pass, db_user, host

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
    file = Column(String(200), default='')
    query: sql.Select


class Done(db.Model):
    __tablename__ = 'done_hw'

    id = Column(Integer, Sequence('done_id_seq'), primary_key=True)
    student_id = Column(Integer)
    homework_id = Column(Integer)
    successful = Column(Boolean, default=False)
    marks = Column(Integer, default=0)
    query: sql.Select


class DBCommands:

    async def get_user(self, user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

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

    async def count_users(self) -> int:
        total = await db.func.count(User.id).gino.scalar()
        return total

    async def count_hw(self) -> int:
        total = await db.func.count(HW.id).gino.scalar()
        return total

    async def show_my_marks(self):
        user_id = types.User.get_current().id
        marks = await Done.query.where(Done.student_id == user_id).gino().all()
        return marks

    async def rate_hw(self, user_id, hw_id, mark):
        current_done = await Done.query.where(Done.student_id == user_id and Done.homework_id == hw_id).gino().first()
        await current_done.update(marks=mark).apply()

    async def done_unmade(self):
        user_id = types.User.get_current().id
        done_unmade_list = await Done.query.where(Done.student_id == user_id and not Done.successful).gino().all()
        return done_unmade_list

    async def unmade_hw(self, homework_id):
        homework = await HW.query.where(HW.id == homework_id).gino().first()
        return homework

    async def list_hw(self):
        hw = await HW.query.gino.all()
        return hw

    async def list_user(self):
        users = await User.query.gino.all()
        return users

    async def list_done(self):
        done = await Done.query.gino.all()
        return done


async def create_db():
    await db.set_bind(f'postgresql://{db_user}:{db_pass}@{host}/gino')
    db.gino: GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()
