from peewee import PostgresqlDatabase, Model, AutoField, IntegerField, CharField, DateTimeField, ForeignKeyField
import datetime

db = PostgresqlDatabase('simple_python_notes_bot',
                        user='friendlyevil',
                        password='friendlyevil',
                        host='localhost',
                        port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Group(BaseModel):
    id = AutoField(primary_key=True)
    user_id = IntegerField()
    name = CharField()
    created_time = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def get_by_user_id(user_id):
        return list(Group.select().where(Group.user_id == user_id))

    @staticmethod
    def get_by_user_and_name(user_id, name):
        return list(Group.select().where(Group.user_id == user_id and Group.name == name))

    @staticmethod
    def create_groups(user_id, group_names):
        groups = [Group(user_id=user_id, name=name) for name in group_names]
        Group.bulk_create(groups)
        return groups


class Note(BaseModel):
    id = AutoField(primary_key=True)
    group = ForeignKeyField(Group, backref='notes')
    message = CharField()
    created_time = DateTimeField(default=datetime.datetime.now)

    @staticmethod
    def get_by_group(group_id):
        return Note.select().where(Note.group == group_id)

    @staticmethod
    def delete_group(group_id):
        return Note.delete().where(Note.group == group_id).execute()


def create_tables():
    with db:
        db.create_tables([Group, Note])
