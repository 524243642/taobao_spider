#!/usr/bin/env python
# encoding: utf-8


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


Base.to_dict = to_dict
