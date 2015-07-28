list=[]
dict1={"name":"nitin", "id":"1"}
dict2={"name":"ankit", "id":"2"}
list.append(dict1)
list.append(dict2)
print list
for sample_list in list:
    print sample_list['name']
    print sample_list['id']
