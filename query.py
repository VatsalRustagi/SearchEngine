import json
import search_utils
from collections import defaultdict
from urlparse import urljoin

class QueryHandler:
    def __init__(self):
        self.cache = {}
        self.bookkeepingMap = self.loadJson()

    def cacheIndex(self, query):
        if query[0] not in self.cache.keys():
            file = open("Indexes/{}.txt".format(query[0]), "r")
            d = dict(eval(file.read()))
            self.cache[query[0]] = d

        if query in self.cache[query[0]].keys():
            return self.cache[query[0]][query]

        return None

    def lookupQuery(self, words):
        docIDs = defaultdict(list)
        searches = []
        for word in words:
            if len(word) > 0:
                l = self.cacheIndex(word)
                searches.append(l)
                if l != None:
                    for id, _, tfidf in l:
                        docIDs[id].append([word, tfidf])
            else:
                print("Please enter a valid query.")
        if all([None == s for s in searches]):
            raise QueryNotFound("Did not find a match for {}".format(' '.join(words)))
        return docIDs

    def processInput(self,query):
        userInput = query.lower()
        words = search_utils.simplifyText(userInput).split(" ")
        result = []
        for word in words:
            if word != '':
                result.append(word)
        return result

    def loadJson(self):
        JSON = json.loads(open("WEBPAGES_RAW/bookkeeping.json").read())
        return dict(JSON)

    def rankingAlgorithm(self, info, additionalInfo=None, results=5):
        sortedInfo = sorted(info.keys(), key=lambda k: (-len(info[k]), -sum([l[1] for l in info[k]])/len(info[k]) ))

        result = []

        if len(sortedInfo) < results:
            for i,k in enumerate(sortedInfo,1):
                result.append("http://"+self.bookkeepingMap[k].encode('UTF-8', 'strict'))
        else:
            for i, k in enumerate(sortedInfo[:results], 1):
                result.append("http://"+self.bookkeepingMap[k].encode('UTF-8', 'strict'))

        return result

    def getLinks(self, query, maxResults=5):
        words = self.processInput(query)
        info = self.lookupQuery(words)
        return self.rankingAlgorithm(info=info, results=maxResults)

class QueryNotFound(Exception):
    pass