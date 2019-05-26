# -*- coding:utf-8 -*-
import MeCab
import sys
import glob
import math
import inspect
import pprint

class naivebayes():
	def __init__(self):
		self.vocabularies = set()
		self.word_count = {}
		self.category_count = {}

	def by_mecab(self, text):
		tagger = MeCab.Tagger('-F\s%f[6] -U\s%m -E\\n')
		words = []
		result = tagger.parse(text).strip().replace('\n','').split(' ')
		while result:
			words.append(result.pop(0))
		return tuple(words)
	
	def word_count_up(self, word, category):
		self.word_count.setdefault(category, {})
		self.word_count[category].setdefault(word, 0)
		self.word_count[category][word] += 1
		self.vocabularies.add(word)
	
	def category_count_up(self, category):
		self.category_count.setdefault(category, 0)
		self.category_count[category] += 1
	
	def train(self, doc, category):
		words = self.by_mecab(doc)
		for word in words:
			self.word_count_up(word, category)
		self.category_count_up(category)
	
	def prior_prob(self, category):
		num_of_categories = sum(self.category_count.values())
		num_of_docs_of_the_category = self.category_count[category]
		return num_of_docs_of_the_category / num_of_categories
	
	def num_of_appearance(self, word, category):
		if word in self.word_count[category]:
			return self.word_count[category][word]
		return 0
	
	def word_prob(self, word, category):
		numerator = self.num_of_appearance(word, category) + 1
		denominator = sum(self.word_count[category].values()) + len(self.vocabularies)
		prob = numerator / denominator
		return prob
	
	def score(self, words, category):
		score = math.log(self.prior_prob(category))
		for word in words:
			score += math.log(self.word_prob(word, category))
		return score
	
	def classify(self, doc):
		best_guessed_category = None
		max_prob_before = -sys.maxsize
		words = self.by_mecab(doc)

		for category in self.category_count.keys():
			prob = self.score(words, category)
			pprint.pprint([category, prob])
			if prob > max_prob_before:
				max_prob_before = prob
				best_guessed_category = category
		return best_guessed_category

def location(depth=1):
	frame = inspect.currentframe().f_back
	return frame.f_lineno

if __name__ == '__main__':
	nb = naivebayes()

train_list = glob.glob('data/*.txt')

for train in train_list:
	file_name = train
	with open(file_name, "r") as f:
		texts = f.read()
		texts_list = texts.split("\n")
	label_name = file_name[5:-4]
	# print(len(texts_list))
	cnt = 0
	for text in texts_list:
		cnt += 1
		# print(cnt)
		nb.train(text, label_name)

text = 'お腹空いたなぁ'
print('メンヘラ判定：　%s' % (nb.classify(text)))

