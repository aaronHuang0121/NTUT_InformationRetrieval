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
        read = r.text.encode('ascii', 'ignore').lower()
        print("24 read: ", read," ",type(read))
        text_tokens = word_tokenize(read) 
        nltk_tokens = [ word for word in text_tokens if not word in stopwords.words()]
        #nltk_tokens = sorted(set(tmp),key=tmp.index)
        ordered_tokens = set()
        tokens_without_sw = []
        for word in nltk_tokens:
            if word not in ordered_tokens:
                ordered_tokens.add(word)
                tokens_without_sw.append(word) 
        check = read.split()
        print("30 check", check)
        for item in tokens_without_sw:
            print("32 item: ", item)
            if item not in output:
                output[item] = {}
                output[item][' total'] = check.count(item)
                output[item][count] = []
                for j in range(1,len(check)+1):
                    if check[j] == item:
                        output[item][count].append(j)
            else:
                output[item][' total'] += check.count(item)
                if count not in output[item]:
                    output[item][count] = []
                for j in range(1,len(check)+1):
                    if check[j] == item:
                        output[item][count].append(j)
            print(output[item])
        count += 1

print(output) 
f= open("output.txt","w+")
f.write(output)