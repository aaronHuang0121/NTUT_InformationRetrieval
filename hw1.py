import warc
import sys
import requests
import io
import nltk 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
nltk.download('stopwords') 
nltk.download('punkt')

documents = []
tokens_without_sw = []
punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~\n'''

f = warc.open("01.warc.gz")
count = 0

for record in f:
    if record.type == 'response':
        print(record.type, " " , record.url)
        r = requests.get(record.url)
        read = r.text.lower()
        documents.append(read)
        text_tokens = word_tokenize(read) 
        tmp = [ word for word in text_tokens if not word in stopwords.words()]
        tmp = sorted(set(tmp),key=tmp.index)
        tokens_without_sw.append(tmp)
        count += 1
        if count == 2:
            break
    
output = {} 
for i in range(0,len(documents)):
    check = documents[i].lower().split()
    print(check)
    for item in tokens_without_sw[i]:
        print(str(item))
        if str(item) not in output:
            output[str(item)] = {}
            output[str(item)][' total'] = check.count(str(item))
            output[str(item)][i+1] = []
            for j in range(0,len(check)):
                if check[j] == item:
                    output[str(item)][i+1].append(j+1)
            print(output[item])
        else:
            output[str(item)][' total'] += check.count(str(item))
            if i+1 not in output[str(item)]:
                output[str(item)][i+1] = []
            for j in range(0,len(check)):
                if check[j] == item:
                    output[str(item)][i+1].append(j+1)
            print(output[item])


print(output) 
