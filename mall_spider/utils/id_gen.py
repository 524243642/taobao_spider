# coding: utf-8
import uuid

from mall_spider.utils.session_id_generator import SessionIdGenerator


class IdGen(SessionIdGenerator):

    @staticmethod
    def uuid():
        return uuid.uuid1().__str__().replace("-", "")

    @staticmethod
    def generate_id(self, session):
        return IdGen.uuid()

    @staticmethod
    def get_next_id():
        return IdGen.uuid()
