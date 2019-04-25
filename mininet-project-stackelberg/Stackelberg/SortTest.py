#-*- encoding=utf-8 -*-   
import operator  
#按字典值排序（默认为升序）  
x = {1:2, 3:4, 4:3, 2:1, 0:0}  
sorted_x = sorted(x.iteritems(), key=operator.itemgetter(1))  
print sorted_x  
#[(0, 0), (2, 1), (1, 2), (4, 3), (3, 4)]  
#如果要降序排序,可以指定reverse=True  
sorted_x = sorted(x.iteritems(), key=operator.itemgetter(1), reverse=True)  
print sorted_x  
#[(3, 4), (4, 3), (1, 2), (2, 1), (0, 0)]  
#或者直接使用list的reverse方法将sorted_x顺序反转  
#sorted_x.reverse()  
  
#取代方法是,用lambda表达式  
sorted_x = sorted(x.iteritems(), key=lambda x : x[1])  
print sorted_x  
#[(0, 0), (2, 1), (1, 2), (4, 3), (3, 4)]  
sorted_x = sorted(x.iteritems(), key=lambda x : x[1], reverse=True)  
print sorted_x  
#[(3, 4), (4, 3), (1, 2), (2, 1), (0, 0)]  
  
#包含字典dict的列表list的排序方法与dict的排序类似,如下：  
x = [{'name':'Homer', 'age':39}, {'name':'Bart', 'age':10}, {'name':'Ball', 'age':30}, {'name':'Chars', 'age':50}]  
sorted_x = sorted(x, key=operator.itemgetter('name'))  
print sorted_x  
#[{'age': 10, 'name': 'Bart'}, {'age': 39, 'name': 'Homer'}]  
sorted_x = sorted(x, key=operator.itemgetter('name'), reverse=True)  
print sorted_x  
#[{'age': 39, 'name': 'Homer'}, {'age': 10, 'name': 'Bart'}]  
sorted_x = sorted(x, key=lambda x : x['name'])  
print sorted_x  
#[{'age': 10, 'name': 'Bart'}, {'age': 39, 'name': 'Homer'}]  
sorted_x = sorted(x, key=lambda x : x['age'], reverse=True)  
print sorted_x  
#[{'age': 39, 'name': 'Homer'}, {'age': 10, 'name': 'Bart'}]