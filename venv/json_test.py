import json
#do zrobienia ladny json#
TT_data= {'issue': [] ,'service': [], 'MGMT': [] }
TT_data['issue'].append("test")
print(TT_data['issue'][len(TT_data['issue'])-1])
json_TT_DATA= json.dumps(TT_data)

print(json_TT_DATA)
print("test")

#print(json_TT_DATA[0]["test"])

all_data= open("osettt_obecne", "r").read()
print(all_data.)