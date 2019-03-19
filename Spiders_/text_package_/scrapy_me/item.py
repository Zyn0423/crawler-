# coding=utf-8
# 构造item对象
class Item(object):
    def __init__(self,data):
        # 设置私有属性
        self._data=data
    @property
    def data(self):
        """
        对外提供访问，一定程度上进行保护
        :return:
        """
        return self._data
