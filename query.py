import json
import search_utils
from collections import defaultdict

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
        for word in words:
            if len(word) > 0:
                l = self.cacheIndex(word)
                for id, _, tfidf in l:
                    docIDs[id].append([word, tfidf])
            else:
                print("Please enter a valid query.")

        return docIDs

    def getInput(self):
        userInput = raw_input("\nEnter Query: ").lower()
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

        if len(sortedInfo) < 5:
            for i,k in enumerate(sortedInfo,1):
                print("{}. {}".format(i, self.bookkeepingMap[k]))
        else:
            for i, k in enumerate(sortedInfo[:5], 1):
                print("{}. {}".format(i, self.bookkeepingMap[k]))

    def run(self):
        while (True):
            words = self.getInput()
            info = self.lookupQuery(words)
            self.rankingAlgorithm(info=info)
            if raw_input("Continue [y/n]? ") == 'n':
                break

QueryHandler().run()

