import enum
from datetime import datetime, timedelta

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import inspect

from app import db


class CommitMixin:

    def commit(self):
        fail_reason = None
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as ex:
            session.rollback()
            fail_reason = ex
        except ValueError as ex:
            session.rollback()
            fail_reason = ex
        finally:
            return self, fail_reason


class DeleteMixin:
    def delete(self):
        try:
            session.delete(self)
            session.commit()
            return None
        except SQLAlchemyError as ex:
            session.rollback()
            return ex
        elass CommitMixin:

    def commit(self):
        fail_reason = None
        try:
            session.add(self)
            session.commit()
        except SQLAlchemyError as ex:
            session.rollback()
            fail_reason = ex
        except ValueError as ex:
            session.rollback()
            fail_reason = ex
        finally:
            return self, fail_reason


class Delxcept ValueError as ex:
            session.rollback()
            return ex


class SyntheticKeyMixin:
    @declared_attr
    def pk(self):
        for base in self.__mro__[1:-1]:
            if getattr(base, '__table__', None) is not None:
                t = ForeignKey(base.pk)
                break
        else:
            t = Integer

        return Column('id', t, primary_key=True)


class HistoryMixin:

    @property
    def history(self):
        state = inspect(self)

        changes = {}

        for attr in state.attrs:
            hist = state.get_history(attr.key, True)

            if not hist.has_changes():
                continue

            old_value = hist.deleted[0] if hist.deleted else None
            new_value = hist.added[0] if hist.added else None
            if old_value != new_value:
                changes[attr.key] = [old_value, new_value]

        return changes


class OrderMixin:
    order_num = Column(Integer(), nullable=True)


class UtcCreatedMixin:
    created = Column(DateTime(), nullable=False, default=datetime.utcnow)


class UserType(enum.Enum):
    lessor = 0
    renter = 1


class Code(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, ):
    __tablename__ = 'verification_codes'

    class Meta:
        enable_in_sai = True
        column_searchable_list = []
        column_filters = []

    target = Column(String(), nullable=False)
    code = Column(String(), nullable=False)
    used = Column(
        Boolean(),
        default=False,
        nullable=False
    )
    expired_at = Column(
        DateTime(),
        nullable=True,
        default=lambda: datetime.utcnow() + timedelta(minutes=5)
    )


class User(Model, DeleteMixin, CommitMixin, HistoryMixin, UtcCreatedMixin):
    __tablename__ = 'users'

    class Meta:
        enable_in_sai = True
        column_searchable_list = []

    pk = Column('id', Integer(), primary_key=True, index=True, unique=True, nullable=False)

    tel = Column(String(), nullable=True)
    login = Column(String(), nullable=True)
    password = Column(String(), nullable=True)
    is_admin = Column(Boolean(), nullable=False, default=False)
    user_type = Column(Enum(UserType), nullable=True)
    avatar = Column(String(), nullable=True)


    passport_photo = Column(String(), nullable=True)
    name = Column(String(), nullable=True)
    passport_issued = Column(String(), nullable=True)
    issue_date = Column(String(), nullable=True)
    department_code = Column(String(), nullable=True)
    passport_series = Column(String(), nullable=True)
    passport_num = Column(String(), nullable=True)
    surname = Column(String(), nullable=True)
    patronymic = Column(String(), nullable=True)
    gender = Column(String(), nullable=True)
    birthdate = Column(String(), nullable=True)
    birthplace = Column(String(), nullable=True)


    token_pairs = relationship('TokenPair', back_populates='user')
    devices = relationship('Device', back_populates='user')
    notifications = relationship('Notification', back_populates='user')
    reviews = relationship('Review', back_populates='user', cascade="all, delete-orphan")
    rooms = relationship('Room', back_populates='user', cascade="all, delete-orphan")
    saved_rooms = relationship('SavedRoom', back_populates='user', cascade="all, delete-orphan", lazy='dynamic')
    block_lists_subject = relationship('BlockList', back_populates='subject', cascade="all, delete-orphan",
                                          foreign_keys='[BlockList.subject_id]')
    block_lists_object = relationship('BlockList', back_populates='object_', cascade="all, delete-orphan",
                                         foreign_keys='[BlockList.object_id]')
    rents = relationship('Rent', back_populates='user', cascade="all, delete-orphan", lazy='dynamic')


class BlockList(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, UtcCreatedMixin):
    __tablename__ = 'block_lists'

    class Meta:
        enable_in_sai = True

    object_id = Column(Integer, ForeignKey(User.pk), nullable=False)
    subject_id = Column(Integer, ForeignKey(User.pk), nullable=False)

    object_ = relationship('User', back_populates='block_lists_object',foreign_keys=[object_id])
    subject = relationship('User', back_populates='block_lists_subject',foreign_keys=[subject_id])


class Token(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, ):
    __tablename__ = 'tokens'

    class Meta:
        enable_in_sai = True

    value = Column(String(), nullable=False)
    expires_at = Column(DateTime(), nullable=False)

    as_refresh = relationship(
        'TokenPair',
        uselist=False,
        back_populates='refresh_token',
        foreign_keys='[TokenPair.refresh_token_id]'
    )
    as_access = relationship(
        'TokenPair',
        uselist=False,
        back_populates='access_token',
        foreign_keys='[TokenPair.access_token_id]'

    )


class TokenPair(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, ):
    __tablename__ = 'token_pairs'

    class Meta:
        enable_in_sai = True

    device = Column(String(), nullable=True)

    user_id = Column(Integer(), ForeignKey(User.pk), nullable=True)

    refresh_token_id = Column(Integer, ForeignKey(Token.pk), nullable=True)
    access_token_id = Column(Integer(), ForeignKey(Token.pk), nullable=True)

    user = relationship(User, back_populates='token_pairs')

    refresh_token = relationship(
        Token,
        foreign_keys=[refresh_token_id],
        back_populates='as_refresh'
    )
    access_token = relationship(
        Token,
        foreign_keys=[access_token_id],
        back_populates='as_access'
    )


class Device(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, ):
    __tablename__ = 'devices'

    class Meta:
        enable_in_sai = True
        column_searchable_list = []
        column_filters = []

    user_id = Column(Integer(), ForeignKey(User.pk), nullable=False)
    firebase_id = Column(String(), nullable=True)
    user_agent = Column(String(), nullable=True)
    enable_notification = Column(Boolean(), nullable=False, default=True)

    user = relationship(User, back_populates='devices')


class Notification(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, ):
    __tablename__ = 'notifications'

    class Meta:
        enable_in_sai = True
        column_searchable_list = []
        column_filters = []

    text = Column(String(), nullable=False)
    created_at = Column(DateTime(), nullable=False, default=datetime.utcnow)
    read = Column(Boolean(), nullable=False, default=False)

    user_id = Column(Integer(), ForeignKey(User.pk), nullable=False)

    user = relationship(User, back_populates='notifications')


class Amenity(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin):
    __tablename__ = 'amenities'

    class Meta:
        enable_in_sai = True
        column_searchable_list = []
        column_filters = []

    name = Column(String, nullable=False)
    icon = Column(String, nullable=False)

    amenity_rooms = relationship('RoomAmenity', back_populates='amenity', cascade="all, delete-orphan")


class Room(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, UtcCreatedMixin):
    __tablename__ = 'rooms'

    class Meta:
        enable_in_sai = True
        column_searchable_list = []
        column_filters = []

    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    humans_count = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    area = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey(User.pk), nullable=False)

    user = relationship(User, back_populates='rooms')
    room_amenities = relationship('RoomAmenity', back_populates='room', cascade="all, delete-orphan")
    attachments = relationship('Attachment', back_populates='room', cascade="all, delete-orphan")
    rents = relationship('Rent', back_populates='room', cascade="all, delete-orphan", lazy='dynamic')
    saved_rooms = relationship('SavedRoom', back_populates='room', cascade="all, delete-orphan", lazy='dynamic')


class RoomAmenity(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, UtcCreatedMixin):
    __tablename__ = 'amenities_rooms'

    class Meta:
        enable_in_sai = True
        column_searchable_list = []
        column_filters = []

    amenity_id = Column(Integer, ForeignKey(Amenity.pk), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.pk), nullable=False)

    amenity = relationship(Amenity, back_populates='amenity_rooms')
    room = relationship(Room, back_populates='room_amenities')


class Attachment(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, UtcCreatedMixin):
    __tablename__ = 'attachments'

    class Meta:
        enable_in_sai = True
        column_searchable_list = []
        column_filters = []

    link = Column(String, nullable=False)
    room_id = Column(Integer, ForeignKey(Room.pk), nullable=False)

    room = relationship(Room, back_populates='attachments')


class Rent(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, UtcCreatedMixin):

    __tablename__ = 'rents'

    class Meta:
        enable_in_sai = True

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    tel = Column(String, nullable=False)
    comment = Column(String, nullable=True)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime,nullable=False)
    room_id = Column(Integer, ForeignKey(Room.pk), nullable=False)
    user_id = Column(Integer, ForeignKey(User.pk), nullable=False)
    verified = Column(Boolean, nullable=True)

    room = relationship(Room, back_populates='rents')
    user = relationship(User, back_populates='rents')
    room_renters = relationship('RoomRenter', back_populates='rent', cascade="all, delete-orphan")
    reviews = relationship('Review', back_populates='rent', cascade="all, delete-orphan", lazy='dynamic')


class RoomRenter(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, UtcCreatedMixin):

    __tablename__ = 'room_renters'

    class Meta:
        enable_in_sai = True

    grown_ups_count = Column(String, nullable=False)
    children_count = Column(String, nullable=False)

    rent_id = Column(Integer, ForeignKey(Rent.pk),nullable=False)
    
    rent = relationship(Rent, back_populates='room_renters')


class Review(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, UtcCreatedMixin):
    __tablename__ = 'reviews'

    class Meta:
        enable_in_sai = True
        column_searchable_list = []
        column_filters = []

    text = Column(String, nullable=True)
    rate = Column(Integer, nullable=True)

    user_id = Column(Integer, ForeignKey(User.pk), nullable=False)
    rent_id = Column(Integer, ForeignKey(Rent.pk), nullable=False)

    user = relationship(User, back_populates='reviews')
    rent = relationship(Rent, back_populates='reviews')


class SavedRoom(Model, SyntheticKeyMixin, DeleteMixin, CommitMixin, HistoryMixin, UtcCreatedMixin):
    __tablename__ = 'saved_rooms'

    class Meta:
        enable_in_sai = True
        column_searchable_list = []
        column_filters = []

    user_id = Column(Integer, ForeignKey(User.pk), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.pk), nullable=False)
    user = relationship(User, back_populates='saved_rooms')
    room = relationship(Room, back_populates='saved_rooms')


