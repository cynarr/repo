import json, os
data = {}
i=0
path = "denews/"
for filename in os.listdir(path):
	s=open(path+filename, 'r').read()
	data[filename] = s

f= open("articles.json","w+")
json_data = json.dumps(data)
f.write(json_data)
f.close()