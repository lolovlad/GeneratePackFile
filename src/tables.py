from sqlalchemy import Column, Integer, String, LargeBinary, \
    Date, ForeignKey, Boolean, Text, Float, UUID

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

base = declarative_base()


class TypeUser(base):
    __tablename__ = "type_user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(32), nullable=False)
    description = Column(String(128), nullable=True)


class User(base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, nullable=False, default=uuid4())

    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    id_type = Column(Integer, ForeignKey("type_user.id"))
    type = relationship("TypeUser", lazy="joined")

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)

    phone = Column(String, nullable=False, unique=True)

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, val):
        self.hashed_password = generate_password_hash(val)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class TypeOrganizations(base):
    __tablename__ = "type_organizations"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(32), nullable=False)
    description = Column(String(128), nullable=True)


class Activity(base):
    __tablename__ = "activity"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(128), nullable=False)
    code = Column(String(32), nullable=False)
    description = Column(String(128), nullable=True)


class Organizations(base):
    __tablename__ = "organizations"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(UUID, default=uuid4())
    name = Column(String(32), nullable=False)
    ogrn = Column(String, nullable=False)
    inn = Column(String, nullable=False)
    kpp = Column(String, nullable=True)
    id_type_organizations = Column(Integer, ForeignKey("type_organizations.id"))
    type_organizations = relationship("TypeOrganizations", lazy="joined")
    date_registration = Column(Date, default=False)
    address = Column(String, nullable=False)
    id_main_activity = Column(Integer, ForeignKey("activity.id"), nullable=True)
    main_activity = relationship("Activity", lazy="joined")
    supervisor = Column(String, nullable=True)
    icon = Column(String, nullable=True, default=None)
    id_user = Column(Integer, ForeignKey("user.id"), nullable=True)


class Tag(base):
    __tablename__ = "tag"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(UUID, default=uuid4())
    id_subtag = Column(Integer, ForeignKey("tag.id"), nullable=True)
    name = Column(String(32), nullable=False)
    description = Column(String(128), nullable=True)


class FileTemplate(base):
    __tablename__ = "file_template"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uuid = Column(UUID, default=uuid4())
    name = Column(String, nullable=False)
    docs = Column(String, nullable=False)
    additional_fields = Column(String, nullable=True, default=None)
    id_tag = Column(Integer, ForeignKey("tag.id"))
    tag = relationship("Tag", lazy="joined")
