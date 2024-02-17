from peewee import SqliteDatabase, Model, CharField, AutoField, ForeignKeyField, DateField, IntegerField
import os


db = SqliteDatabase("database.db")


class BaseModel(Model):
    """Базовая модель в базе данных"""
    class Meta:
        database = db


class User(BaseModel):
    """Модель пользователя"""
    user_id = IntegerField(primary_key=True)
    username = CharField()


class Command(BaseModel):
    """Модель команды"""
    command_id = AutoField()
    command_name = CharField()
    user = ForeignKeyField(User, backref='commands')
    when_requested = DateField()

    def __str__(self):
        return '/{command_name} ({date})'.format(
            command_id=self.command_id,
            command_name=self.command_name,
            date=self.when_requested
        )


def initialize_db():
    """Инициализирует базу данных, создает таблицу, если не создана"""
    db.connect()
    db.create_tables(BaseModel.__subclasses__(), safe=True)
    db.close()



