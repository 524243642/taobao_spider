# coding: utf-8
import json

from sqlalchemy import TypeDecorator, Text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.mutable import Mutable

from config.config_loader import logger


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        """Convert plain dictionaries to MutableDict."""

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        """Detect dictionary set events and emit change events."""

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        """Detect dictionary del events and emit change events."""

        dict.__delitem__(self, key)
        self.changed()


@MutableDict.as_mutable
class JSONEncodedMutableDict(TypeDecorator):
    """Represents an mutable structure as a json-encoded string.

    Usage::

        JSONEncodedMutableDict(255)

    """

    impl = Text

    def process_bind_param(self, value, dialect):
        if value:
            value = json.dumps(value, ensure_ascii=False, indent=2)
        else:
            value = None

        return value

    def process_result_value(self, value, dialect):
        if value:
            value = json.loads(value)
        else:
            value = {}

        return value


class JSONEncodedLongColumn(TypeDecorator):
    impl = LONGTEXT

    def process_bind_param(self, value, dialect):
        try:
            value = json.dumps(value, ensure_ascii=False, indent=2)
        except BaseException as e:
            logger.exception(e)
            value = ''
        return value

    def process_result_value(self, value, dialect):
        try:
            value = json.loads(value)
        except BaseException:
            value = {}
        return value


class JSONEncodedColumn(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        try:
            value = json.dumps(value, ensure_ascii=False, indent=2)
        except BaseException as e:
            logger.exception(e)
            value = ''
        return value

    def process_result_value(self, value, dialect):
        try:
            value = json.loads(value)
        except BaseException:
            value = {}
        return value


def bit_column_helper(offset, name='status'):
    """a helper to turn a bit of an integer field to be a flag,
    see DeleteBitMixin for an example
    @param offset index of the bit, from lower to higher, starts from 0
    @param name name of the column
    """

    mask = 1 << offset

    class BitHelper(object):

        def enable(self):
            value = getattr(self, name)
            value |= mask
            setattr(self, name, value)

        def disable(self):
            value = getattr(self, name)
            value &= ~mask
            setattr(self, name, value)

        def is_enable(self):
            value = getattr(self, name)
            return bool(value & mask)

        @staticmethod
        def is_set_criterion():
            def _(cls):
                column = getattr(cls, name)
                return column.op('&')(mask) != 0

            return classmethod(_)

        def set_value(self, is_enable):
            value = getattr(self, name)
            if is_enable:
                value |= mask
            else:
                value &= ~mask
            setattr(self, name, value)

        bit_property = property(is_enable, set_value)

    return BitHelper
