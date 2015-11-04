import re
import sys
from collections import Counter

import mechanize 
from bs4 import BeautifulSoup
from lxml.html.clean import Cleaner
import nltk
# Might need to uncomment below if not already installed 
# nltk.download()


from nltk.corpus import stopwords
from urllib2 import urlopen, Request

# Method that gets all the relative links from google from our defined search
def getArticles(keyword):
	cleaner = Cleaner()
	cleaner.javascript = True
	cleaner.style = True

	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.addheaders=[('User-agent','chrome')]

	term = keyword.replace(" ", "+")
	query = "http://www.google.ca/search?&tbm=nws&num=10&q=" + term 
	htmltext = br.open(query).read()
	#print htmltext

	soup = BeautifulSoup(htmltext)

	search = soup.findAll('div', attrs={'id': 'search'})
	#print search[0]
	searchtext= str(search[0])
	soup1=BeautifulSoup(searchtext)
	list_items=soup1.findAll('li')

	regex = "q=.*?&amp"	
	pattern = re.compile(regex)
	results_array = []
	for li in list_items:
		soup2 = BeautifulSoup(str(li))
		links = soup2.findAll('a')
		source_link = links[0]
		#print source_link
		source_url = re.findall(pattern, str(source_link))
		if len(source_url) > 0:
				results_array.append(str(source_url[0].replace("q=", "").replace("&amp", "")))
	return results_array
# Get's all the important data (in paragraph tags), parses it, 
# splits it, and retrieves the top 100 common words escaping stop words
def parser(results_array):
	result = []
	stop = stopwords.words('english')
	hdr = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'})
	for url in results_array:
		all_text = ""
		text_data = urlopen(Request(url, headers= hdr)).read().decode('unicode_escape').encode('ascii','ignore')
		for paragraph in re.findall(r'<p>(.*?)</p>', text_data):
			all_text += re.sub(r'<([^>]+)>', '', paragraph)
		top_words= [ite for ite, it in Counter(all_text.split(' ')).most_common(100) if ite not in stop]
		#print top_words
			#print all_text
		result.append(top_words)		
	return result

#	Create a list of candidate item sets of size one.
def createCan(dataset):
    c1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    #frozenset because it will be a key of a dictionary.
    return map(frozenset, c1)

# Returns all candidates that meets a minimum support level
def scanData(dataset, candidates, min_support):
    sscnt = {}
    for tid in dataset:
        for can in candidates:
            if can.issubset(tid):
                sscnt.setdefault(can, 0)
                sscnt[can] += 1

    num_items = float(len(dataset))
    retlist = []
    support_data = {}
    for key in sscnt:
        support = sscnt[key] / num_items
        if support >= min_support:
            retlist.insert(0, key)
        support_data[key] = support
    return retlist, support_data

# Generate the joint transactions from candidate sets
def aprioriGenenerate(freq_sets, k):
    retList = []
    lenLk = len(freq_sets)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(freq_sets[i])[:k - 2]
            L2 = list(freq_sets[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(freq_sets[i] | freq_sets[j])
    return retList

# Generate a list of candidate item sets
def apriori(dataset, minsupport=0.5):
    C1 = createCan(dataset)
    D = map(set, dataset)
    L1, support_data = scanData(D, C1, minsupport)
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGenenerate(L[k - 2], k)
        Lk, supK = scanData(D, Ck, minsupport)
        support_data.update(supK)
        L.append(Lk)
        k += 1

    return L, support_data

# Change mimsupport to whatever you want to search for. 
def main():
	keyword = raw_input("Please enter what you would like to search: ")
	#minsupp = raw_input("Please enter min Support: ")
	articles_info = getArticles(keyword)
	topWords = parser(articles_info)
	#print topWords
	L = apriori(topWords)
	L, support_data = apriori(topWords, minsupport=0.3)
	print L

if __name__ == '__main__':
	main()