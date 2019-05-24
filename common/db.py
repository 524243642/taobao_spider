#!/usr/bin/env python
# encoding: utf-8

import traceback
from contextlib import contextmanager
from functools import partial

from sqlalchemy import create_engine, event
from sqlalchemy.exc import DisconnectionError
from sqlalchemy.orm import sessionmaker

from config.config_loader import logger, global_profile


def checkout_listener(dbapi_con, con_record, con_proxy):
    try:
        try:
            dbapi_con.ping(False)
        except TypeError:
            dbapi_con.ping()
    except dbapi_con.OperationalError as exc:
        if exc.args[0] in (2006, 2013, 2014, 2045, 2055):
            raise DisconnectionError()
        else:
            raise


_write_engine = create_engine(global_profile.SQLALCHEMY_DATABASE_URI, pool_recycle=3600)
_read_engine = create_engine(global_profile.SQLALCHEMY_DATABASE_URI_R, pool_recycle=3600)
# Pessimistic
event.listen(_write_engine, 'checkout', checkout_listener)
event.listen(_read_engine, 'checkout', checkout_listener)
_Session = sessionmaker()


@contextmanager
def _session_scope(engine, **kwargs):
    session = _Session(bind=engine, **kwargs)
    try:
        yield session
        session.commit()
    except:
        logger.error("failed to finish the commit: %s", traceback.format_exc())
        session.rollback()
        raise
    finally:
        session.close()


write_session_scope = partial(_session_scope, _write_engine)
read_session_scope = partial(_session_scope, _read_engine)
