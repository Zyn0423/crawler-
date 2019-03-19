# coding=utf-8
# 管道组件
# 负责处理数据对象(Item)
class Pipeline(object):
    '''负责处理数据对象(Item)'''
    def process_item(self,item):
        '''处理item对象'''
        return print({'item':item})
