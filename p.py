import re 
import pandas as pd 
from datetime import datetime

f = open('grp.txt' , 'r' , encoding ='utf-8')
data = f.read()

#print(data)
pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[A-Za-z][A-Za-z]\s-\s'
mess = re.split(pattern , data)[1:]
#print(mess)

dates = re.findall(pattern , data)

modified_dates = []
for x in dates :
	x=x.replace("am" , "AM")
	x= x.replace("pm" , "PM")
	x= x.replace("," , "")
	x= x.replace("\u202f" , " ")
	x =datetime.strptime(x,"%d/%m/%Y %I:%M %p - ")
	modified_dates.append(x)


df = pd.DataFrame({'user_message':mess, 'date':modified_dates})
#print(df)


users = []
messages = []
for message in df['user_message']:
	entry = re.split('([\w\W]+?):\s' , message)
	if entry[1:]:
		users.append(entry[1])
		messages.append(entry[2])
	else : 
		users.append('group_notification')
		messages.append(entry[0])

df['users']=users
df['message']=messages
df.drop(columns=['user_message'] ,  inplace=True)
df['year']=df['date'].dt.year
df['month']= df['date'].dt.month_name()
df['day']=df['date'].dt.day
df['hour']=df['date'].dt.hour
df['minute']=df['date'].dt.minute

print(df)