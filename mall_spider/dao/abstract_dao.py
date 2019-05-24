# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from mall_spider.dao.utils import make_query, fill_model


class AbstractDao(object):
    def __init__(self, model_cls=None, session=None):
        self.model_cls = model_cls
        self.session = session

    @property
    def base_query(self):
        """
        查询操作请使用base_query
        :return:
        """
        return make_query(self.model_cls, self.session)

    def query_one(self, group_by=None, order_by=None, entities=None, _filter=None, for_update=False, **kwargs):
        """
        :param for_update:
        :param group_by:
        :param order_by:
        :param _filter:
        :param entities:
        :param kwargs:
        :return:
        """
        query = self.base_query.filter_by(**kwargs).filter(_filter).group_by(group_by).order_by(
            order_by).with_entities(
            entities)
        if for_update:
            query = query.with_for_update()
        return query.first()

    def query(self, group_by=None, order_by=None, entities=None, _filter=None, for_update=False, **kwargs):
        """
        :param for_update:
        :param group_by:
        :param order_by:
        :param _filter:
        :param entities:
        :param kwargs:
        :return:
        """
        query = self.base_query.filter_by(**kwargs).filter(_filter).group_by(group_by).order_by(
            order_by).with_entities(
            entities)
        if for_update:
            query = query.with_for_update()
        return query.all()

    def insert(self, **kwargs):
        """
        :param kwargs:
        :return:
        """

        entity = self.model_cls()
        fill_model(entity, kwargs)
        self.session.add(entity)
        self.session.flush()
        return entity

    def insert_entity(self, entity):
        self.session.add(entity)
        self.session.flush()
        return entity

    def bulk_insert(self, data_dict_list):
        entities = [self.model_cls(**e) for e in data_dict_list]
        self.session.add_all(entities)
        # self.session.bulk_insert_mappings(self.model_cls, data_dict_list)
        self.session.flush()
        return entities

    def update(self, mod_dict, _filter=None, **kwargs):
        """

        :param kwargs:
        :param mod_dict:
        :param _filter:
        :return:
        """

        entities = self.base_query.filter_by(**kwargs).filter(_filter).all()
        if entities:
            for entity in entities:
                fill_model(entity, mod_dict)
            self.session.flush()

    def delete(self, _filter=None, **kwargs):
        return self.base_query.filter(_filter).filter_by(**kwargs).delete()

    def bulk_delete(self, entities):
        id_list = [e.id for e in entities]
        self.delete(_filter=[self.model_cls.id.in_(id_list)])
        self.session.flush()

    @classmethod
    def get_instance(cls):
        return cls()
