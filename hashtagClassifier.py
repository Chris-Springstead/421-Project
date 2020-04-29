import os, sys
import numpy as np
from tweetLoader import loadTweets
from enum import IntEnum
import math
import operator

class Labels(IntEnum):
	sad = 0
	happy = 1
	shy = 2
	social = 3
	introvert = 4
	extrovert = 5

class hashtagClasifier:
	def __init__(self):
		# total number of tweets
		self.n_tweet_total = 0
		# total number of tweets for each label/class
		self.n_tweet = {l: 0 for l in Labels}
		# frequency of words for each label
		self.vocab = {l: {} for l in Labels}
		self.s = set()

	def train(self, tweets):
		#print(len(tweets))
		# getting total number of tweets
		#print(self.n_tweet)
		self.n_tweet_total = len(tweets)
		for tweet in tweets:
			# adding number of tweets for each label
			curr_label = int(tweets[tweet].label)
			self.n_tweet[Labels(curr_label)] = self.n_tweet[Labels(curr_label)]+1

			# making term freq vectors
			words = tweets[tweet].tString.split(" ")
			for word in words:
				if word not in self.vocab[Labels(curr_label)]:
					self.vocab[Labels(curr_label)][word] = 1
				else:
					val = self.vocab[Labels(curr_label)][word]
					val += 1
					self.vocab[Labels(curr_label)][word] = val
				self.s.add(word)
		

	def predict(self, query):
		# split given query on words
		#print(query)
		words = query.split(" ")
		vals = {l: 0 for l in Labels}
		for l in Labels:
			log_like = 0
			prior = self.n_tweet[l] / self.n_tweet_total
			count = 0

			for item in self.vocab[l]:
				count += self.vocab[l].get(item)

			for word in words:
				if word in self.vocab[l]:
					wc = self.vocab[l][word] + 1
				else:
					wc = 1
					
				total_wc = count + abs(len(self.s) + 1)
				likelihood = wc/total_wc
				log_like += math.log(likelihood)
			
			vals[l] = math.log(prior) + log_like
		#print(vals)
		return max(vals.items(), key=operator.itemgetter(1))[0]
	
def evaluate(model, tweets):
	totalTests = 0
	numRight = 0
	
	l0Got = 0
	l1Got = 0
	l2Got = 0
	l3Got = 0
	l4Got = 0
	
	l0Right = 0
	l1Right = 0
	l2Right = 0
	l3Right = 0
	l4Right = 0

	l0Relevant = 0
	l1Relevant = 0
	l2Relevant = 0
	l3Relevant = 0
	l4Relevant = 0
	for tweet in tweets:
		#print(model.predict(tweets[tweet].tString))

		predictedLabel = model.predict(tweets[tweet].tString)
		#print(str(predictedLabel) + " " + str(tweets[tweet].label))
		totalTests += 1

		#Accuracy = num right / total
		if predictedLabel == Labels(int(tweets[tweet].label)):
			numRight += 1

		#precision = TP / (TP + FP)
		if predictedLabel == Labels(0):
			l0Got += 1
			if predictedLabel == Labels(int(tweets[tweet].label)):
				l0Right += 1
		elif predictedLabel == Labels(1):
			l1Got += 1
			if predictedLabel == Labels(int(tweets[tweet].label)):
				l1Right += 1
		elif predictedLabel == Labels(2):
			l2Got += 1
			if predictedLabel == Labels(int(tweets[tweet].label)):
				l2Right += 1
		elif predictedLabel == Labels(3):
			l3Got += 1
			if predictedLabel == Labels(int(tweets[tweet].label)):
				l3Right += 1
		elif predictedLabel == Labels(4):
			l4Got += 1
			if predictedLabel == Labels(int(tweets[tweet].label)):
				l4Right += 1

		#recall = TP / (TP + FN)

		l0Relevant = l0Got - l0Right
		l1Relevant = l1Got - l1Right
		l2Relevant = l2Got - l2Right
		l3Relevant = l3Got - l3Right
		l4Relevant = l4Got - l4Right
	
	#print(str(l0Got) + " " + str(l0Right) + " " + str(l0Relevant))

	#F1 = 2 / (1/P + 1/R)
	accuracy = numRight / totalTests
	print("Accuracy: ", accuracy, '\n')

	l0precision = l0Right / (l0Right + l0Got)
	l0recall = l0Right / (l0Right + l0Relevant)
	l0F1 = 2 / ((1/l0precision) + (1/l0recall))
	print(str(Labels(0)) + " Precision: ", l0precision)
	print(str(Labels(0)) + " Recall: ", l0recall)
	print(str(Labels(0)) + " F1: ", l0F1, '\n')

	l1precision = l1Right / (l1Right + l1Got)
	l1recall = l1Right / (l1Right + l1Relevant)
	l1F1 = 2 / ((1/l1precision) + (1/l1recall))
	print(str(Labels(1)) + " Precision: ", l1precision)
	print(str(Labels(1)) + " Recall: ", l1recall)
	print(str(Labels(1)) + " F1: ", l1F1, '\n')

	l2precision = l2Right / (l2Right + l2Got)
	l2recall = l2Right / (l2Right + l2Relevant)
	l2F1 = 2 / ((1/l2precision) + (1/l2recall))
	print(str(Labels(2)) + " Precision: ", l2precision)
	print(str(Labels(2)) + " Recall: ", l2recall)
	print(str(Labels(2)) + " F1: ", l2F1, '\n')

	l3precision = l3Right / (l3Right + l3Got)
	l3recall = l3Right / (l3Right + l3Relevant)
	l3F1 = 2 / ((1/l3precision) + (1/l3recall))
	print(str(Labels(3)) + " Precision: ", l3precision)
	print(str(Labels(3)) + " Recall: ", l3recall)
	print(str(Labels(3)) + " F1: ", l3F1, '\n')

	l4precision = l4Right / (l4Right + l4Got)
	l4recall = l4Right / (l4Right + l4Relevant)
	l4F1 = 2 / ((1/l4precision) + (1/l4recall))
	print(str(Labels(4)) + " Precision: ", l4precision)
	print(str(Labels(4)) + " Recall: ", l4recall)
	print(str(Labels(4)) + " F1: ", l4F1, '\n')

def driver(query):
	trainDict = loadTweets("HashtagTweets")
	hasT = hashtagClasifier()
	hasT.train(trainDict)
	predictedLabel = hasT.predict(query)
	#print(predictedLabel)
	return "Predicted Label: " + str(predictedLabel)


def main():
	tweets = loadTweets("HashtagTweets")
	print(len(tweets))
	trainTweets = {}
	testTweets = {}
	#print(tweets)
	index = 0
	for key in tweets.keys():
		if index%10 == 0:
			testTweets[key] = tweets[key]
		else:
			trainTweets[key] = tweets[key]
		index += 1
	
	hashT = hashtagClasifier()
	hashT.train(trainTweets)
	evaluate(hashT, testTweets)

if __name__ == "__main__":
	main()

