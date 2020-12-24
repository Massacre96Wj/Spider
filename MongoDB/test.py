# -*- coding: UTF-8 -*-
"""
@Author ：WangJie
@Date   ：2020/12/2 10:00 
@Desc   ：
"""

import pymongo

# 1.连接
client = pymongo.MongoClient(host="127.0.0.1", port=27017)
# 或者
client = pymongo.MongoClient("mongodb://localhost:27017/")

# 2.创建 db
db = client.test
# 或者
db = client['test']

# 3.集合
collection = db.students
# 或者
collection = db['students']

# 4.插入单条数据
student = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}
student1 = {
    'id': '20170101',
    'name': 'Jordan',
    'age': 20,
    'gender': 'male'
}
student2 = {
    'id': '20170202',
    'name': 'Mike',
    'age': 21,
    'gender': 'male'
}
result = collection.insert_one(student)
# 插入多条数据
result = collection.insert_many([student1, student2])

# 5.查询数据
result = collection.find_one({"name": 'Mike'})

# 查询多条数据,返回生成器，for打印结果
result = collection.find({'age': 20})

# 运算符，大于
result = collection.find({'age': {'$gt': 20}})
''':arg
    小于：{'age': {'$lt': 20}}
    大于：{'age': {'$gt': 20}}
    小于等于：{'age': {'$lte': 20}}
    大于等于：{'age': {'$gte': 20}}
    不等于：{'age': {'$ne': 20}}
    在范围内：{'age': {'$in': [20, 23]}}
    不在范围内：{'age': {'$nin': [20, 23]}}
'''

# 正则
result = collection.find({'name': {'$regex': '^M.*'}})
''':arg
    $exists属性是否存在      {'name': {'$exists': True}}name属性存在
    $type类型判断            {'age': {'$type': 'int'}} age的类型为int
    $mod数字模操作           {'age': {'$mod': [5, 0]}}年龄模5余0
    $text文本查询            {'$text': {'$search': 'Mike'}}text类型的属性中包含Mike字符串
    $where高级条件查询       {'$where': 'obj.fans_count == obj.follows_count'}自身粉丝数等于关注数
    https://docs.mongodb.com/manual/reference/operator/query
'''
# 计数
count = collection.find().count()
count = collection.find({'age': 20}).count()        # collection.count_documents({'age': 20})

# 排序(ASCENDING, DESCENDING)
result = collection.find().sort('name', pymongo.DESCENDING)

# 偏移,忽略前两个元素， limit限制个数
result = collection.find().sort('name', pymongo.ASCENDING).skip(2).limit(2)

# 6.更新数据
student = collection.find_one({'name': 'Mike'})
student['age'] = 19
result = collection.update_one({'name': 'Mike'}, {'$set': student})

# 实例
condition = {'age': {'$gt': 20}}
result = collection.update_one(condition, {'$inc': {'age': 1}})
print(result)
print(result.matched_count, result.modified_count)

condition = {'age': {'$gt': 20}}
result = collection.update_many(condition, {'$inc': {'age': 1}})
print(result)
print(result.matched_count, result.modified_count)

# 7.删除,remove不推荐使用
result = collection.remove({'name': 'Mike'})
# delete_one()即删除第一条符合条件的数据，delete_many()即删除所有符合条件的数据
result = collection.delete_one({'name': 'Kevin'})
print(result)
print(result.deleted_count)
result = collection.delete_many({'age': {'$lt': 25}})
print(result.deleted_count)
# http://api.mongodb.com/python/current/api/pymongo/collection.html