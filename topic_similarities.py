import sys
import sqlite3
conn = sqlite3.connect('../uofadata.db')


authors = conn.execute("SELECT rowid, auid, name, researcharea FROM authorsummary WHERE rowid <= "+sys.argv[1])

topics = set()
topics_of_person = list()
for author in authors:
	#split the research area line
	#trim it
	#get all the research topics
	#check whether two topics are mentioned by same people
	#generate pairwise matrix counitng number of times they appear together
	research_areas = set()
	for phrase in author[3].split(","):
		t = phrase.strip().lower()
		if t != '':
			research_areas.add(t)
	topics_of_person.append(research_areas)
	for r in research_areas:
		#if r in topics:print r
		topics.add(r)

n = 0
index = dict()
inv_index = list()
for x in topics:
	inv_index.append(x)
	index[x] = n
	n = n + 1

similarity = list()
for i in range(n):
	similarity.append(list())
	for j in range(n):
		similarity[i].append(0)

for x in topics:
	for y in topics:
		if x!=y:
			for i in range(len(topics_of_person)):
				if ((x in topics_of_person[i]) and (y in topics_of_person[i])):
					similarity[index[x]][index[y]] = similarity[index[x]][index[y]] + 1

#for i in range(n):
#	for j in range(i+1,n):
#		if similarity[i][j]>1:print(inv_index[i]+","+inv_index[j])

#increase the weight
for i in range(n):
	for j in range(n):
		similarity[i][j] = similarity[i][j]*1

import numpy as np
U, s, V = np.linalg.svd(similarity, full_matrices=True)
#print U
#print s
sig = np.zeros(shape=(n, 2))
import math
sig[0][0] = math.sqrt(s[0])
sig[1][1] = math.sqrt(s[1])
out_arr = np.dot(U,sig)
print(out_arr)
import matplotlib.pyplot as plt
plt.plot(out_arr[:,0], out_arr[:,1], "o")
plt.show()
