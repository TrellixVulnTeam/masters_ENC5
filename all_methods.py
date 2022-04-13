from sklearn.cluster import DBSCAN
import numpy as np
import json 
import pickle
import math
import re
import random
from collections import Counter
from build_index import Index
from scipy import spatial
import time




# ssh steved7@acidburn.cs.rpi.edu


def KL(vec1, vec2):
	p = np.asarray(vec1)
	q = np.asarray(vec2)
	p  = p  / np.linalg.norm(p )
	q = q / np.linalg.norm(q)
	epsilon = 0.00001
	p = p+epsilon
	q = q+epsilon
	divergence = np.sum(p*np.log(p/q))
	return divergence 



f = open('data/info.json')
info = json.load(f)

with open('all_data.pkl', 'rb') as inp:
    inn = pickle.load(inp)

with open('embeddings.pkl', "rb") as fIn:
	    stored_data = pickle.load(fIn)
	    stored_order = stored_data['order']
	    stored_embeddings = stored_data['embeddings']


embedded_dict = {}
temp_order = []
temp_embeddings = []
n = 100#sys.argv[1]
rand_idxs = random.sample(range(0, 2000), n)
for i in rand_idxs: #filter out 
	embedded_dict[stored_order[i]] = stored_embeddings[i]
	temp_order.append(stored_order[i])
	temp_embeddings.append(stored_embeddings[i])

stored_order = temp_order
stored_embeddings = temp_embeddings


clustering = DBSCAN(eps=.30, min_samples=7, metric='cosine').fit(stored_embeddings)


lst = clustering.labels_

#print(clustering.labels_)
print(max(clustering.labels_))
print(np.count_nonzero(clustering.labels_ != -1))
print(np.count_nonzero(clustering.core_sample_indices_ != -1))
	

clusters = {}
for i in range(len(clustering.labels_)):
	temp = clustering.labels_[i]
	if(temp != -1):
		if(temp in clusters.keys()):
			clusters[temp].append(stored_order[i])
		else:
			clusters[temp] = [stored_order[i]]


tfidf = {}
for word in inn.doc_sim_score.keys(): 
	
	count = 0
	for doc in inn.doc_sim_score[word]:
		if(doc[1] != 0):
			count += 1

	if(count <= 1): #filter out single words 
		continue

	for doc in inn.doc_sim_score[word]:
		if(doc[0] in tfidf.keys()): 
			tfidf[doc[0]].append(doc[1])
		else:
			tfidf[doc[0]]= [doc[1]]



##### baseline cosine tf-idf #####
number = 0
base_clust = []
base_set = set()
start = time.time()
tmp = stored_order.copy()
while(len(tmp) > 1):

	idx = random.randrange(0,len(tmp))
	cent = tmp.pop(idx)
	j = 0
	first = True
	while(j < len(tmp)):
		dist = (1-spatial.distance.cosine(tfidf[cent], tfidf[tmp[j]] ))
		if(dist > .8):
			if(first):
				base_clust.append([cent])
				base_set.add(cent)
				number += 1
			first = False
			base_clust[-1].append(tmp[j])
			base_set.add(tmp[j])
			tmp.pop(j)
			number+=1

		else:
			j+=1

end = time.time()
print("Baseline cosine tf-idf: " + str(end - start))
print("Number of articles flagged (BASELINE): " + str(number))

sources = set()
for i in base_set:
	sources.add(info[i]['source'])

print("Number of sources (BASELINE): ", end = '')
print(len(sources))

print("Number of clusters: ",end ='')
print(len(base_clust))



##### baseline KL tf-idf #####
number = 0
base_clust = []
base_set = set()
start = time.time()
tmp = stored_order.copy()
while(len(tmp) > 1):

	idx = random.randrange(0,len(tmp))
	cent = tmp.pop(idx)
	j = 0
	first = True
	while(j < len(tmp)):
		dist = KL(tfidf[cent], tfidf[tmp[j]])
			if(dist < 10.0):
			if(first):
				base_clust.append([cent])
				base_set.add(cent)
				number += 1
			first = False
			base_clust[-1].append(tmp[j])
			base_set.add(tmp[j])
			tmp.pop(j)
			number+=1

		else:
			j+=1

end = time.time()
print()
print("Baseline KL tf-idf: " + str(end - start))
print("Number of articles flagged (BASELINE): " + str(number))

sources = set()
for i in base_set:
	sources.add(info[i]['source'])

print("Number of sources (BASELINE): ", end = '')
print(len(sources))

print("Number of clusters: ",end ='')
print(len(base_clust))


##### baseline cosine bert #####
number = 0
base_clust = []
base_set = set()
start = time.time()
tmp = stored_order.copy()
while(len(tmp) > 1):

	idx = random.randrange(0,len(tmp))
	cent = tmp.pop(idx)
	j = 0
	first = True
	while(j < len(tmp)):
		dist = (1-spatial.distance.cosine(embedded_dict[cent], embedded_dict[tmp[j]] ))
		if(dist > .8):
			if(first):
				base_clust.append([cent])
				base_set.add(cent)
				number += 1
			first = False
			base_clust[-1].append(tmp[j])
			base_set.add(tmp[j])
			tmp.pop(j)
			number+=1

		else:
			j+=1

end = time.time()
print("Baseline cosine BERT: " + str(end - start))
print("Number of articles flagged (BASELINE): " + str(number))

sources = set()
for i in base_set:
	sources.add(info[i]['source'])

print("Number of sources (BASELINE): ", end = '')
print(len(sources))

print("Number of clusters: ",end ='')
print(len(base_clust))

##### baseline KL bert #####
number = 0
base_clust = []
base_set = set()
start = time.time()
tmp = stored_order.copy()
while(len(tmp) > 1):

	idx = random.randrange(0,len(tmp))
	cent = tmp.pop(idx)
	j = 0
	first = True
	while(j < len(tmp)):
		dist = KL(embedded_dict[cent], embedded_dict[tmp[j]])
			if(dist < 10.0):
			if(first):
				base_clust.append([cent])
				base_set.add(cent)
				number += 1
			first = False
			base_clust[-1].append(tmp[j])
			base_set.add(tmp[j])
			tmp.pop(j)
			number+=1

		else:
			j+=1

end = time.time()
print("Baseline KL BERT: " + str(end - start))
print("Number of articles flagged (BASELINE): " + str(number))

sources = set()
for i in base_set:
	sources.add(info[i]['source'])

print("Number of sources (BASELINE): ", end = '')
print(len(sources))

print("Number of clusters: ",end ='')
print(len(base_clust))

#cluster bert, cosine tf-idf
#cluster bert, KL tf-idf
#cluster bert, cosine bert
#cluster bert, KL bert








