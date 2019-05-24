# coding: utf-8

class Good(dict):
    meta = {
        'flag': '1',
        'categoryId': '淘宝品类id',
        'categoryName': '淘宝品类name',
        'brandId': '淘宝品牌id',
        'brandName': '淘宝品牌name',
        'modelId': '淘宝型号id',
        'modelName': '淘宝型号name',
        'priceInfo': [{
            'skuId': '淘宝skuId',
            'price': '淘宝真实价格'
        }],
        'sellCount': '淘宝销量',
        'date': '2018-10-27'
    }

    def set_flag(self, flag):
        self['flag'] = flag
        return self

    def get_flag(self):
        return self['flag']

    def set_category_id(self, category_id):
        self['categoryId'] = category_id
        return self

    def get_category_id(self):
        return self['categoryId']

    def set_category_name(self, category_name):
        self['categoryName'] = category_name
        return self

    def set_brand_id(self, brand_id):
        self['brandId'] = brand_id
        return self

    def get_brand_id(self):
        return self['brandId']

    def set_brand_name(self, brand_name):
        self['brandName'] = brand_name
        return self

    def get_brand_name(self):
        return self['brandName']

    def set_model_id(self, model_id):
        self['modelId'] = model_id
        return self

    def set_model_name(self, model_name):
        self['modelName'] = model_name
        return self

    def get_model_name(self):
        return self['modelName']

    def get_query(self):
        return self['brandName'] + '+' + self['modelName']

    def set_price_info(self, price_info):
        self['priceInfo'] = price_info
        return self

    def set_sell_count(self, sell_count):
        self['sellCount'] = sell_count
        return self

    def set_date(self, date):
        self['date'] = date
        return self

    def get_date(self):
        return self['date']

    def set_sku_base(self, sku_base):
        self['skuBase'] = sku_base
        return self

    def get_sku_base(self):
        return self['skuBase']
