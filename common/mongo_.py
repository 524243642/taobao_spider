# -*- coding: utf-8 -*-
import traceback
from contextlib import contextmanager

from pymongo import MongoClient

from config.config_loader import global_profile, logger

mongo_client = MongoClient(global_profile.MONGO_DATABASE_URI)
db = mongo_client.get_database(global_profile.MONGO_DB)


@contextmanager
def mongo_collection_scope(**kwargs):
    collection_name = kwargs.get('collection_name')
    try:
        collection = db.get_collection(name=collection_name)
        yield collection
    except:
        logger.error("failed to finish the mongo commit: %s", traceback.format_exc())
        raise
