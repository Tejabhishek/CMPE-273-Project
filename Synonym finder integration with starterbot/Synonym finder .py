import unicodedata    
from PyDictionary import PyDictionary
dictionary=PyDictionary()

list= ['professor','assistant','lecturer','fellow','tutor']
final1=[]


command= 'associate'

for i in list:
 list1=dictionary.synonym(i)
 list1 = [str(i).strip() for i in list1]

 final1.append(list1)


if command in final1[0] or command in final1[1] or final1[2] or command in final1[3]  or command in final1[4] :

 print "sucess"









