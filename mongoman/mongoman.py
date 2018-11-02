import atexit
from prodict import Prodict
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import logging

logger = logging.getLogger('MongoMan')
logger.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler(__name__ + '.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

__all__ = ['MongoMan', logger]


class TempSuper(Collection):
    # def __init__(self) -> None:
    #     super().__init__()
    #     self.super_find_one = super().find_one
    #     self.super_find = super().find

    def find_one(self, filter=None, *args, **kwargs):
        return super().find_one(filter, *args, **kwargs)

    def find(self, *args, **kwargs):
        return super().find(*args, **kwargs)


class ModeledCollection(Collection):
    def __init__(self, database, name, create=False, codec_options=None, read_preference=None, write_concern=None,
                 read_concern=None, session=None, **kwargs):
        super().__init__(database, name, create, codec_options, read_preference, write_concern, read_concern, session,
                         **kwargs)
        self._model = None
        self._temp_super = TempSuper(database, name, create, codec_options, read_preference, write_concern,
                                     read_concern, session,
                                     **kwargs)
        self.super_find = self._temp_super.find
        self.super_find_one = self._temp_super.find_one

    def set_model(self, model: type(Prodict) = Prodict):
        self._model = model

    def get_model(self):
        return self._model

    def find_one(self, model: type(Prodict) = None, filter=None, *args, **kwargs):
        cursor = self.super_find_one(filter, *args, **kwargs)
        final_model = model or self.get_model()
        if final_model is None:
            return cursor
        if cursor is not None:
            return final_model.from_dict(cursor)

    def find(self, model: type(Prodict) = None, *args, **kwargs):
        iterator = self.super_find(*args, **kwargs)
        final_model = model or self.get_model()
        if final_model is None:
            for it in iterator:
                yield it
        else:
            for it in iterator:
                yield final_model.from_dict(it)


class MongoMan:
    __default_instance = None

    def __init__(self, host='localhost', port=27017, db='test', user=None, password=None, auth_db='admin',
                 auto_connect=True):
        logger.debug('__init__')
        self._host = host
        self._port = port
        self._db_name = db
        self._user = user
        self._password = password
        self._auth_db: str = auth_db
        self._connection: MongoClient = None
        self._db: Database = None
        self._connected = False
        self._use_uri = False
        self._collection_models = {}
        MongoMan.__default_instance = self
        # self.__instance_id = uuid.uuid4()
        # # log.debug('MongoManager instance id={}'.format(self.instance_id()))
        if auto_connect:
            logger.debug('Auto connect is on.')
            self.connect()

    @property
    def host(self):
        return self._host

    @property
    def db(self):
        return self._db

    @property
    def auth_db(self):
        return self._auth_db

    @property
    def port(self):
        return self._port

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def connection(self):
        return self._connection

    @property
    def connected(self):
        return self._connected

    @classmethod
    def default_instance(cls):
        return cls.__default_instance

    @classmethod
    def has_default_instance(cls):
        if cls.__default_instance is None:
            return False
        return True

    def connect(self):
        logger.debug('Connecting...')
        if self.connected:
            logger.warning('MongoDB connection is already open. Using existing connection...')
            return self.db

        self._connection = MongoClient(self._host, self._port)
        # mongodb: // user_name: user_password @ SERVER_IP / prod - db
        # uri = 'mongodb://{}:{}@{}:{}/{}'.format(self.user, self.password, self.host, self.port, self.db_name)
        # self.connection = MongoClient(uri)
        if self._user and self._password:
            auth_db = self._connection[str(self._auth_db)]
            auth_db.authenticate(self._user, self._password)

        self._db = self.connection[self._db_name]
        if self.db is not None:
            self._connected = True

        return self.db

    def collection(self, collection_name, model: type(Prodict) = Prodict) -> ModeledCollection:
        coll = ModeledCollection(self.db, collection_name)
        coll.set_model(model)
        return coll

    def close(self):
        logger.debug('close() called')
        self.connection.close()
        self._connected = False


@atexit.register
def close_connection():
    logger.debug('at exit: Closing MongoDB connection...')
    if MongoMan.has_default_instance():
        if MongoMan.default_instance().connected:
            MongoMan.default_instance().close()
