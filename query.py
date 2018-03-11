import json

def query(map):
    while (True):
        word = raw_input("Enter Query: ").lower()
        if len(word) > 0:
            file = open("Indexes/{}.txt".format(word[0]), "r")
            d = dict(eval(file.read()))
            if word in d.keys():
                l = sorted(d[word], key= lambda x: (-x[2]))[:5]
                for i, details in enumerate(l,1):
                    print("{}. {}".format(i, map[details[0]]))
            else:
                print("Couldn't find the word")

        continue_loop = raw_input("Continue the program? ['q' to quit] : ")
        if continue_loop == 'q':
            return

def loadJson():
    JSON = json.loads(open("WEBPAGES_RAW/bookkeeping.json").read())
    return dict(JSON)

urlMap = loadJson()
query(urlMap)