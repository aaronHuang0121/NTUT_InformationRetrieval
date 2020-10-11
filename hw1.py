import warc
import sys
import requests
import io
import nltk 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
nltk.download('stopwords') 
nltk.download('punkt')


punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~\n='''
count = 1
output = {} 

f = warc.open("01.warc.gz")

for record in f:
    if record.type == 'response':
        print "21 record.type: ", record.type, " , record.url: " , record.url
        r = requests.get(record.url, verify=False)
        read = r.text.encode('ascii', 'ignore').lower()
        print "\n\n\n24  ",type(read)," read: ", read
        text_tokens = word_tokenize(read) 
        nltk_tokens = [ word for word in text_tokens if not word in stopwords.words()]
        print "\n\n\n27 nltk_tokens: ",nltk_tokens
        #tmp = sorted(set(tmp),key=tmp.index)
        ordered_tokens = set()
        tokens_without_sw = []
        for word in nltk_tokens:
            if word not in ordered_tokens:
                ordered_tokens.add(word)
                tokens_without_sw.append(word) 
        print "\n\n\n28 tokens_without_sw: ",tokens_without_sw
        check = read.split()
        print "\n\n\n30 check", check
        for item in tokens_without_sw:
            print "\n\n\n32 item: ", item
            if item not in output:
                output[item] = {}
                output[item][' total'] = check.count(item)
                output[item][count] = []
                for j in range(0,len(check)):
                    if check[j] == item:
                        output[item][count].append(j+1)
            else:
                output[item][' total'] += check.count(item)
                if count not in output[item]:
                    output[item][count] = []
                for j in range(0,len(check)):
                    if check[j] == item:
                        output[item][count].append(j+1)
            print(output[item])
        print "\n\n\n48 output", output
        count += 1

print "\n\n\n50 output: ", output 

f= open("output.txt","w+")
f.write(output)
