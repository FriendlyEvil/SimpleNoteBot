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
    def create_note_in_new_group(user_id, group_name, message):
        return Note.create(group=Group.create(user_id=user_id, group_name=group_name).id,
                           message=message)


def create_tables():
    with db:
        db.create_tables([Group, Note])


DEFAULT_GROUPS = ['favourites', 'todo', 'watch later']


def get_groups_or_create_default(user_id):
    groups = Group.get_by_user_id(user_id)
    if groups:
        return groups
    return Group.create_groups(user_id, DEFAULT_GROUPS)
