import json
import search_utils

class QueryHandler:
    def __init__(self):
        self.cache = {}
        self.bookkeepingMap = self.loadJson()

    def cacheIndex(self, query):
        if query[0] not in self.cache.keys():
            file = open("Indexes/{}.txt".format(query[0]), "r")
            d = dict(eval(file.read()))
            self.cache[query[0]] = d
        else:
            if query in self.cache[query[0]].keys():
                l = sorted(self.cache[query[0]][query], key=lambda x: (-x[2]))[:5]
                for i, details in enumerate(l, 1):
                    print("{}. {}".format(i, self.bookkeepingMap[details[0]]))
            else:
                print("Couldn't find the word")

    def lookupQuery(self, words):
        for word in words:
            if len(word) > 0:
                self.cacheIndex(word)
            else:
                print("Please enter a valid query.")


    def getInput(self):
        userInput = raw_input("Enter Query: ").lower()
        words = search_utils.simplifyText(userInput).split(" ")
        result = []
        for word in words:
            if word != '':
                result.append(word)
        return result

    def loadJson(self):
        JSON = json.loads(open("WEBPAGES_RAW/bookkeeping.json").read())
        return dict(JSON)

    def run(self):
        while (raw_input("Continue [y/n]?") != 'n'):
            words = self.getInput()
            self.lookupQuery(words)


QueryHandler().run()

