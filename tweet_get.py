#!/usr/local/var/pyenv/shims/python
# -*- coding: utf-8 -*-

import json
import sys
import glob
import os
import subprocess
from requests_oauthlib import OAuth1Session
import pprint

CK = os.environ.get("TWITTER_CK")
CS = os.environ.get("TWITTER_CS")
AT = os.environ.get("TWITTER_AT")
AS = os.environ.get("TWITTER_AS")

session = OAuth1Session(CK, CS, AT, AS)

def screen_name_list(file):
	# 読み込み用データとして、fileを開いて読み込む
	f = open(file, "r", encoding="utf-8").read()
	# 改行コード(\n)で区切ってリスト化(配列化)する
	screen_name = f.split("\n")
	return screen_name

train_list = glob.glob('list/*.txt')

os.makedirs("data", exist_ok=True)

for train in train_list:
	screen_names = screen_name_list(train)
	for screen_name in screen_names:
		url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
		params = {'screen_name':screen_name, 'count':200}
		response = session.get(url, params = params)
		response_text = json.loads(response.text)

		texts = []
		#for data in response_text:
		#	texts.append(data['text'])
		#pprint.pprint(texts)
		texts = [data.get('text') for data in response_text]
		#pprint.pprint(texts)
		#exit()
		data_name = str(train).replace('list', 'data', 1)

		with open(data_name, "a") as f:
			for text in texts:
				f.write(str(text) + "\n")


