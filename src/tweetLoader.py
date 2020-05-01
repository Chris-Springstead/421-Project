import csv
from datetime import datetime
import re
import glob

def removeEmoji(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

class tweet:
    tString = " "
    likes = 0
    date = 0 
    retweets = 0 
    links = []
    label = 0

def __repr__(self):
        return (tString)

#all tweets stored in this dictionary
#each key is the tweet ID
#each value is the tweet class above
tweetDictionary = {}

def loadTweets(subFile):
    for folder in glob.glob("TweetsFolder/"):
        for file in glob.glob(folder + "*.csv"):
            with open(file , encoding='cp437') as csvfile:
                readCSV = csv.reader(csvfile, delimiter=',')
                firstline = True
                for row in readCSV:
                    #print(row[7])
                    if firstline and row[0] == "tweets":
                        firstline = False
                        continue
                    else:
                        firstline = False 
                    #currently the csv format os
                    #0 - tweet      1 - id     2 - len
                    #3 - mm/dd/yyyy 4 - source 5 - likes
                    #6 - retweets   7 - label
                    newTweet = tweet()
                    #need to filter the tweet of caps and grammar and stuff 
                    tweetString = removeEmoji(row[0])
                    link = re.search(r'http\S+', tweetString)
                    if link != None:
                        #print(link.group(0))
                        newTweet.links.append(link.group(0))
                    tweetString = re.sub(r'http\S+', '', tweetString)
                    tweetString = re.sub(r'\r\n', " ", tweetString)
                    tweetString = re.sub(r'\'' , "" , tweetString)
                    tweetString = re.sub(r"[^a-zA-Z@_0-9]+", " ", tweetString)
                    tweetString = re.sub(r'[" "]+', " ", tweetString)
                    tweetString = tweetString.lower()
                    newTweet.tString = tweetString
                    newTweet.likes = row[5]
                    newTweet.retweets = row[6]
                    if (subFile == "HashtagTweets"):
                        newTweet.label = row[7]
                    date = (row[3].split(" "))
                    YMD = date[0]
                    date = datetime.strptime(YMD, '%Y-%m-%d')
                    newTweet.date = date
                    id = row[1]
                    #duplicate checking 
                    if id not in tweetDictionary:
                        tweetDictionary[id] = newTweet
    return (tweetDictionary)


def main():
    print("Loading Tweets")
    dict = loadTweets("*")
    print(len(dict.keys()))
    print("Finished Loading Tweets")
    return
            
if __name__ == "__main__":
    main()
