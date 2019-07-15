import json

data = {'name':'Da Ye','number':100,'age':78}
jsonStr = json.dumps(data)  #python数据结构(一般为字典)转换为JSON编码的字符串
print(jsonStr)
print(type(json))
data2 = json.loads(jsonStr) #将一个JSON编码的字符串转换回一个python数据结构
print(data2)
print(type(data2))
#写入json类型数据
with open("my_data.json",'w',encoding="utf-8") as f:
	json.dump(data2,f)

#读入json类型数据
with open("my_data.json",'r',encoding="utf-8") as g:
	result_data = json.load(g)
print(result_data)
