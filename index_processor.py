from nltk import FreqDist, word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from collections import defaultdict
from pathlib2 import Path
import time
import search_utils

STOPWORDS = set(stopwords.words("english"))
Alphabets = defaultdict(lambda: defaultdict(list))

def processFile(r, tags):
    soup = BeautifulSoup(r, "html.parser")
    all_tags = soup.find_all(tags)
    corpus = []
    all_Text = ""

    for i in all_tags:
        text = i.get_text().lower()
        all_Text += " " + search_utils.simplifyText(text)

    words = word_tokenize(all_Text)

    for word in words:
        if word not in STOPWORDS:
            corpus.append(word.encode('UTF-8', 'strict'))

    freqDict = FreqDist(corpus)
    return freqDict

def writeToFile():
    unique_words = 0
    for k,v in Alphabets.items():
        unique_words += len(v.keys())
        indexFile = open("Indexes/{}.txt".format(k), "w")
        indexFile.write(str(dict(v)))
        indexFile.close()
    print("\nUnique Words : {}".format(unique_words))

def processDictionary(freqDict, folder, fileNum):
    for term, tf in dict(freqDict).items():
        Alphabets[term[0]][term].append(["{}/{}".format(folder,fileNum), tf, 0])

def updateWithTFIDF(TOTAL_DOCUMENTS):
    for letter, dictionary in Alphabets.items():
        for token, l in dictionary.items():
            for i in range(len(l)):
                tf = dictionary[token][i][1]
                dictionary[token][i][2] = search_utils.calculate_tfidf(tf, len(l), TOTAL_DOCUMENTS)

def processIndex():
    total_time = time.time()
    done_folders = []
    TOTAL_DOCUMENTS = 0
    path = Path("WEBPAGES_RAW")
    for folder in path.iterdir():
        if folder.is_dir():
            folderNum = folder.stem
            for file in folder.iterdir():
                if not file.is_dir():
                    fileNum = file.stem
                    try:
                        r = open(str(file), "r")
                        freqDict = processFile(r, ["h1","h2","h3","strong","b","title","body"])
                        processDictionary(freqDict, folderNum, fileNum)
                        r.close()
                        TOTAL_DOCUMENTS += 1
                    except:
                        raise
            done_folders.append(int(folderNum))
            print(sorted(done_folders))
            print("Ran for {}".format(time.time() - total_time))
    updateWithTFIDF(TOTAL_DOCUMENTS)
    writeToFile()
    print("Total Documents : {}".format(TOTAL_DOCUMENTS))
    print("\nThe process ran for {}".format(time.time() - total_time))

processIndex()
