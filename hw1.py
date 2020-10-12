import warc
import sys
import requests
import io
import nltk 
import time
import os
import json
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
nltk.download('stopwords') 
nltk.download('punkt')

punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~\n='''
count = 1
output = {} 
if not os.path.isdir("./output"): os.mkdir("./output")

f = warc.open("01.warc.gz")
for record in f:
    if record.type == 'response':
        try:
            t1 = time.time()
            print "21 record.type: ", record.type, " , record.url: " , record.url
            r = requests.get(record.url, verify=False, headers={'Connection':'close'})
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
                if item not in output:
                    output[item] = {}
                    output[item][' total'] = check.count(item)
                    output[item][count] = []
                    for j in range(0,len(check)):
                        if check[j] == item:
                            output[item][count].append(j+1)
                            print "\n\n\n32 item: ", item, ": ", output[item]
                else:
                    output[item][' total'] += check.count(item)
                    if count not in output[item]:
                        output[item][count] = []
                    for j in range(0,len(check)):
                        if check[j] == item:
                            output[item][count].append(j+1)
                            print "\n\n\n32 item: ", item, ": ", output[item]
            print "\n\n\n48 count " , count ,"; output: ", output
            f2= open("./output/output_" +  time.strftime("%Y%m%d%H%M%S", time.localtime())+ ".json","w+")
            json.dump(output, f2)
            f2.close
            print '\n\n\ntime elapsed: ' + str(round(time.time()-t1, 2)) + ' seconds'
            count += 1
        except:
            print("An exception occurred")

print "\n\n\n50 output: ", output
f2= open("./output/output_" +  time.strftime("%Y%m%d%H%M%S", time.localtime())+ ".json","w+")
json.dump(output, f2)
f2.close
f.close