import warc
import sys
import requests
import io
import nltk 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
nltk.download('stopwords') 
nltk.download('punkt')


punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~\n'''
count = 1
output = {} 

f = warc.open("01.warc.gz")

for record in f:
    if record.type == 'response':
        print("21 record.type: ", record.type, " , record.url: " , record.url)
        r = requests.get(record.url)
        read = r.text.lower()
        print("24 read: ", read)
        text_tokens = word_tokenize(read) 
        tmp = [ word for word in text_tokens if not word in stopwords.words()]
        tmp = sorted(set(tmp),key=tmp.index)
        tokens_without_sw = tmp
        check = read.split()
        print("30 check", check)
        for item in tokens_without_sw:
            print("32 str(item): ", str(item))
            if str(item) not in output:
                output[str(item)] = {}
                output[str(item)][' total'] = check.count(str(item))
                output[str(item)][count] = []
                for j in range(1,len(check)+1):
                    if check[j] == item:
                        output[str(item)][count].append(j)
            else:
                output[str(item)][' total'] += check.count(str(item))
                if count not in output[str(item)]:
                    output[str(item)][count] = []
                for j in range(1,len(check)+1):
                    if check[j] == item:
                        output[str(item)][count].append(j)
            print(output[item])
        count += 1

print(output) 
