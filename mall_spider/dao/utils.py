# -*- coding: utf-8 -*-

"""
  dao帮助类
"""

from __future__ import absolute_import, print_function

import copy

from sqlalchemy import desc
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.schema import Column
from sqlalchemy.sql.expression import ColumnElement


def get_model_pks(model_cls):
    rtn = set()
    if hasattr(model_cls, '_sa_class_manager'):
        class_manager = getattr(model_cls, '_sa_class_manager')
        if hasattr(class_manager, 'mapper'):
            mapper = getattr(class_manager, 'mapper')
            if hasattr(mapper, '_all_pk_props'):
                pks = getattr(mapper, '_all_pk_props')
                if pks:
                    for pk in pks:
                        rtn.add(getattr(pk, 'description'))
    else:
        for key in model_cls.__dict__:
            item = getattr(model_cls, key, None)
            if item is not None and isinstance(item, Column) and hasattr(item, 'primary_key') and item.primary_key:
                rtn.add(item.name)
    return rtn


def get_model_onupdates(model_cls):
    rtn = {}
    properties = _extract_model_properties(model_cls)
    for pro in properties:
        column = getattr(model_cls, pro)
        try:
            onupdate = getattr(column, 'onupdate')
            if onupdate is not None:
                rtn[pro] = onupdate
        except AttributeError:
            pass
    return rtn


def fill_model(_model, _conditions):
    _, conditions = _unpack_conditions(type(_model), _conditions)
    properties = _extract_model_properties(type(_model))
    fill_properties = list(set(properties).intersection(set(conditions.keys())))
    for prop in fill_properties:
        value = conditions.get(prop)
        if isinstance(value, (list, dict, tuple, set)):
            value = copy.deepcopy(value)
        setattr(_model, prop, value)


def copy_model_ignore_properties(_model_target, _model_source, *args):
    properties = _extract_model_properties(type(_model_target))
    for prop in properties:
        if args and prop not in args and hasattr(_model_source, prop):
            setattr(_model_target, prop, getattr(_model_source, prop))


def copy_model(_model_target, _model_source):
    copy_model_ignore_properties(_model_target, _model_source)


def _merge_condition(model_cls, _conditions):
    equals_dict = dict()
    scope_dict = dict()
    in_dict = dict()

    format_conditions, _ = _unpack_conditions(model_cls, _conditions)

    def set_condition(k, v):
        if isinstance(v, (list, set, tuple)):
            in_dict[k] = v
        else:
            equals_dict[k] = v

    for prop, value in format_conditions.items():
        set_condition(prop, value)

    return equals_dict, scope_dict, in_dict


def _unpack_conditions(model_cls, _conditions):
    rtn_cond = dict()
    key_cond = dict()
    for k in _conditions.keys():
        if isinstance(k, Column):
            key = k.name
            prop = getattr(model_cls, key, None)
        elif isinstance(k, InstrumentedAttribute):
            key = k.key
            prop = k
        # elif isinstance(k, (str, unicode)):
        elif isinstance(k, (str)):
            key = k
            prop = getattr(model_cls, k, None)
        else:
            continue

        v = _conditions.get(k)
        if prop:
            rtn_cond[prop] = v
            key_cond[key] = v
    return rtn_cond, key_cond


def _unpack_entities(model_cls, entities):
    rtn = []
    for entity in entities:
        rtn.append(_unpack_entity(model_cls, entity))
    return rtn


def _unpack_entity(model_cls, source):
    if isinstance(source, Column) and source.name:
        return getattr(model_cls, source.name)
    # elif isinstance(source, (str, unicode)):
    elif isinstance(source, (str)):
        return getattr(model_cls, source)
    else:
        return source


def _extract_model_properties(model_cls):
    if hasattr(model_cls, '_sa_class_manager'):
        class_manager = getattr(model_cls, '_sa_class_manager')
        if class_manager:
            if hasattr(class_manager, '_all_key_set'):
                return list(getattr(class_manager, '_all_key_set'))
            elif hasattr(class_manager, 'keys'):
                return class_manager.keys()
    else:
        rtn = list()
        attr_names = model_cls.__dict__
        for attr_name in attr_names:
            v = getattr(model_cls, attr_name)
            if isinstance(v, InstrumentedAttribute):
                rtn.append(attr_name)
        return rtn


def _with_entities(model_cls, entities, query):
    if not isinstance(entities, (set, list, tuple)):
        entities = (entities,)
    else:
        if len(entities) == 0:
            return []
    actual_entities = _unpack_entities(model_cls, entities)
    if actual_entities:
        query = query.with_entities(*actual_entities)
        return query


def _filter_equals(query, filter_dict):
    for k in filter_dict.keys():
        v = filter_dict.get(k)
        query = query.filter(k == v)
    return query


def _filter_scope(query, item, range_p):
    if range_p.begin is not None:
        if range_p.begin_equals:
            query = query.filter(item >= range_p.begin)
        else:
            query = query.filter(item > range_p.begin)
    if range_p.end is not None:
        if range_p.end_equals:
            query = query.filter(item <= range_p.end)
        else:
            query = query.filter(item < range_p.end)
    return query


def _filter_in(query, filter_dict):
    for k in filter_dict.keys():
        v = filter_dict.get(k)
        query = query.filter(k.in_(v))
    return query


def _order_by(query, model_cls, order_by):
    if not isinstance(order_by, (list, tuple)):
        order_bys = (order_by,)
    else:
        order_bys = order_by
    for order_by_ in order_bys:
        if order_by_ is not None:
            # if isinstance(order_by_, (str, unicode)) and order_by_.startswith('-'):
            if isinstance(order_by_, (str)) and order_by_.startswith('-'):
                query = query.order_by(desc(order_by_[1:]))
            else:
                order_by_ = _unpack_entity(model_cls, order_by_)
                query = query.order_by(order_by_)
    return query


def _group_by(query, model_cls, group_by):
    if not isinstance(group_by, (list, tuple)):
        group_bys = (group_by,)
    else:
        group_bys = group_by
    for group_by_ in group_bys:
        if group_by_ is not None:
            group_by_ = _unpack_entity(model_cls, group_by_)
            query = query.group_by(group_by_)
    return query


def _check_param(*args, **kwargs):
    for arg in args:
        if arg is not None:
            return True
    for v in kwargs.values():
        if v:
            return True
    return False


class _Query(object):

    def __init__(self, model_cls, session):
        self._model_cls = model_cls
        self._session = session
        self._query = self._session.query(model_cls)
        self._exception = None

    def with_entities(self, entities):
        if entities is not None:
            self._query = _with_entities(self._model_cls, entities, self._query)
        return self

    def order_by(self, order_by):
        if order_by is not None:
            self._query = _order_by(self._query, self._model_cls, order_by)
        return self

    def group_by(self, group_by):
        if group_by is not None:
            self._query = _group_by(self._query, self._model_cls, group_by)
        return self

    def limit(self, limit_):
        if limit_ is not None:
            self._query = self._query.limit(limit_)
        return self

    def offset(self, offset_):
        if offset_ is not None:
            self._query = self._query.offset(offset_)
        return self

    def filter_by(self, **kwargs):
        if kwargs:
            equals_dict, scopes_dict, in_dict = _merge_condition(self._model_cls, kwargs)
            if equals_dict:
                self._query = _filter_equals(self._query, equals_dict)
            if in_dict:
                self._query = _filter_in(self._query, in_dict)
            if scopes_dict:
                for k in scopes_dict.keys():
                    v = scopes_dict.get(k)
                    self._query = _filter_scope(self._query, k, v)
        return self

    def filter(self, filters_):
        if filters_ is not None:
            if isinstance(filters_, (tuple, list, set)):
                for filter_ in filters_:
                    self._query = self._query.filter(filter_)
            elif isinstance(filters_, ColumnElement):
                self._query = self._query.filter(filters_)
        return self

    def count(self):
        from sqlalchemy import func
        pks = get_model_pks(self._model_cls)
        entities = []
        for pk in pks:
            entities.append(getattr(self._model_cls, pk))
        return self._query.with_entities(func.count(*entities)).scalar()

    def with_for_update(self):
        return self._query.with_for_update()

    def all(self):
        return self._query.all()

    def first(self):
        return self._query.first()

    def exists(self):
        return self._query.exists()

    def delete(self):
        rtn = self._query.all()
        self._query.delete(synchronize_session=False)
        self._session.expire_all()
        return rtn

    def scalar(self):
        return self._query.scalar()


def make_query(model_cls, _session):
    return _Query(model_cls, _session)
