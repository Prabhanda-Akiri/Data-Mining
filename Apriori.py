import csv
import numpy as np
from itertools import chain
from itertools import combinations

# min support-2 to 5, min confidence-50%
def main():

	f_no=input('\nChoose the data file\n1. test_dataset_1.csv \n2. retail_dataset.csv \n')
	
	dataset=read_file(f_no)
	#print(dataset)
	dataset=dataset[:50]
	items=get_items(dataset)
	#print(items)

	L_freq_itemsets=apply_apriori(dataset,items,min_sup=2)
	generate_association_rules(dataset,items,f_no,L_freq_itemsets,confidence=0.5)

	#itemsets,max_cand=create_itemsets(dataset,items)
	#print(itemsets[1],max_cand)
	#print(dataset.count(['I1']))
	'''alphabets = ['a', 'b', 'c']
	for (a,b) in combinations(alphabets, 2):
	    print(a+b)'''

def generate_association_rules(dataset,items,f_no,L_freq_itemsets,confidence=0.5):

	k=int(input('\nEnter k value for kth itemset for association rules:\n'))

	if len(L_freq_itemsets)<(k) or L_freq_itemsets[k-1]==None:
		print('No frequent itemset exists for value ',k)
		return

	association_list=L_freq_itemsets[k-1]
	combs=[]

	for iter_i in range(len(association_list)):

		for iter_j in range(k):
			#pass
			l1=list(combinations(association_list[iter_i],iter_j))

			for m in range(len(l1)):
				p=[]
				p.append(l1[m])
				p.append(get_remaining(association_list[iter_i],l1[m]))
				combs.append(p)

	rules=combs
	size=len(combs)
	c1=[0 for i in range(size)]
	c2=[0 for i in range(size)]

	for i in range(len(dataset)):
		for j in range(size):
			
			if all(elem in dataset[i] for elem in combs[j][0]):
				c1[j]+=1
			if all(elem in dataset[i] for elem in combs[j][1]):
				c2[j]+=1

	for i in range(size):
		if (c2[i]/c1[i])<0.5:
			rules[i]=None
		else:
			print(rules[i])


def get_remaining(p,q):

	rm=[]
	for i in range(len(p)):
		if p[i] in q:
			continue
		else:
			rm.append(p[i])

	return rm 

def apply_apriori(dataset,items,min_sup):
	#pass

	#finding length of the longest transaction
	m=len(max(dataset, key=lambda col1: len(col1)))

	L_freq_itemsets=[]
	C_candidate_itemsets=[]
	C_sup_count=[]

	for i in range(m):

		C_candidate_itemsets.append(create_itemsets(items,i+1))
		L_freq_itemsets.append([])

		#print(C_candidate_itemsets[i])
		no_of_k=len(C_candidate_itemsets[i])
		C_sup_count.append([0 for j in range(no_of_k)])

		for iter_items in range(no_of_k):
			for iter_dataset in range(len(dataset)):
				result= all(elem in dataset[iter_dataset] for elem in C_candidate_itemsets[i][iter_items])
				#print(C_candidate_itemsets[i][iter_items],dataset[iter_dataset],result)
				if result:
					C_sup_count[i][iter_items]+=1

			if C_sup_count[i][iter_items]>=min_sup:
				L_freq_itemsets[i].append(C_candidate_itemsets[i][iter_items])

		#print(C_candidate_itemsets[i],C_sup_count[i])

		#----if number of frquent itemsets in kth itemset is 0 then breaking the algo
		if(len(L_freq_itemsets[i])==0):
			break


	print(C_candidate_itemsets,'\n',L_freq_itemsets)
	return L_freq_itemsets


def create_itemsets(items,k):
	#pass
	return list(combinations(items,k))

def get_items(dataset):

	#converting 2d list od input data into 1d list
	data=list(chain.from_iterable(dataset))

	#returning distinct items from 1d list
	return sorted(list(set(data)))

def read_file(f_no):

	if f_no=='1':
		f_name='test_dataset_1.csv'
	else:
		f_name='retail_dataset.csv'
	
	data=[]
	with open(f_name, 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			if not row:
				continue
			data.append(row)

	return data 

if __name__ == '__main__':
	main()
