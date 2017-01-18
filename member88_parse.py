import os
import sys

with open('/Users/duntex/Wooooops/member88.html') as f:
    lines = f.readlines()
print("""
<html>
<body>
<table>
""")

lst = []

for line in lines:
    #try:
        pic_url = line.split("><br><a")[0].split("<img src=")[1]
        tmp = line.split("<a href=")[1]
        rapid_link = tmp.split("\">")[0] + "\""
        title = tmp.split("\">")[1].split("/</a>")[0]
        prod_id = title.split(' ')[0]
        d = {'id': prod_id, 'title': title[1:], 'img_url': pic_url, 'rapid_url': rapid_link}
        #print("Title: {}".format(title))
        #print("PID: {}".format(prod_id))
        lst.append(d)
    #except Exception as e:
    #    print(line)
lst.sort()
count = 0
row_size = 6
for ele in lst:
    path = '/Users/duntex/acd/Sorted/{}/{}/{}'.format(ele['id'][0], ele['id'].split('-')[0], ele['id'])
    if os.path.exists(path):
        continue
    if count % row_size == 0:
        print("<tr>")
    
    content = '<a target="_blank" href="https://www.javbus.com/{}"><img src={} title="{}"/></a><br><a href={}>{}</a>'.format(ele['id'], ele['img_url'], ele['title'], ele['rapid_url'], ele['id'])
    print('<th>{}</th>'.format(content))   
    
    if count % row_size == row_size - 1:
        print("</tr>")
    count += 1

print("""
</table>
</body>
</html>
""")
