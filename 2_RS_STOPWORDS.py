from nltk import punkt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from csv import reader
import csv
import re
import pandas as pd
#,encoding="utf8" ,encoding="latin1"
fechita="_0721"
opened_file=open("D:/Documents/Proyectos SAS/Ruby --- Paco/Redes Sociales/PY/RS_NEG{}_SINCS2.csv".format(fechita),encoding="utf8")
read_file=reader(opened_file)
read_file
apps_data=list(read_file)
print(apps_data[:5])
print(len(apps_data))

stopwords=set(stopwords.words("spanish"))
stopwords.discard("como")
stopwords.discard("cual")
stopwords.discard("antes")
stopwords.discard("ante")
stopwords.discard("cuando")
stopwords.discard("donde")
stopwords.discard("que")
##print(stopwords)

i=0
a=''
for word in apps_data[1:]:
    words=word_tokenize(word[3])
    filtro=[]
    for w in words:
        if w not in stopwords:
            filtro.append(w)

    separador = " "
    #union=separador.join(filtro)
    word[3]=separador.join(filtro)
    if i<5:
        print(filtro)
        i+=1
dataframes=pd.DataFrame(apps_data)
#,encoding="utf8"
dataframes.to_csv("D:/Documents/Proyectos SAS/Ruby --- Paco/Redes Sociales/PY/RS{}SINCSSTOP.csv".format(fechita),index=False,header=False)
#print the data without stopwords in the texto field
print("Final")
 
'''
csv.register_dialect('myDialect',quoting=csv.QUOTE_ALL,skipinitialspace=True)

with open('C:/Users/DULCE/Documents/BIGML/REDES SOCIALES/BASE/RS_0120SINCSSTOP.csv', 'w', newline='') as f:
    writer = csv.writer(f, dialect='myDialect')
    for row in apps_data:
        writer.writerow(row)

f.close()

 

stop_words_lst = ['yo', 'so', 'well', 'um', 'a', 'the', 'you know', 'i mean']
s = "you know what i mean so just turn the lights on"

import re
for w in stop_words_lst:
    pattern = r'\b'+w+r'\b'
    s = re.sub(pattern, '', s)
    print (s)
'''
