#wapa
Webpage Analysis with Apriori Algo

The purpose of wapa, was to be able to query any information we want, retrieve it, parse it, then try to make sense of it all with the Apriori Algorithm. The Apriori Algorithm is an influential algorithm for mining frequent itemsets for boolean association rules.  

## About

What wapa does is, that you enter a search, with that search you crawl google and retrieve the latest 10 articles/webpages written about that subject (Note you can change this number to whatever you want). Wapa grabs all the important data, parses it, makes it look nice, and then splits everyword. Then we place each webpage information in it's own "dataset", taking into regard the top 50 words used on each webpage (can be changed, or removed) disregarding [Stop Words](https://en.wikipedia.org/wiki/Stop_words). In this case we have 10 datasets. 

Now with all this, we now us the Apriori Algorithm to try to make sense of it all

MinSupport is defaulted to 0.3. Can change it in main:
```
def main():
	keyword = raw_input("Please enter what you would like to search: ")
	articles_info = getArticles(keyword)
	topWords = parser(articles_info)
	L = apriori(topWords)
	# change it here
	L, support_data = apriori(topWords, minsupport=0.3)
	print L
```
## Usage
To Run : 
```
python wapa.py
```
License
-------
MIT-License

-------

