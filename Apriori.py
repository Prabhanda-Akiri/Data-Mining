import csv
import numpy as np
from itertools import chain
from itertools import combinations
# min support-2 to 5, min confidence-50%
def main():

	f_no=input('\nChoose the data file\n1. test_dataset_1.csv \n2. retail_dataset.csv \n')
	
	dataset=read_file(f_no)
	print(dataset)
	items=get_items(dataset)
	print(items)
	apply_apriori(dataset,items,min_sup=2)
	#itemsets,max_cand=create_itemsets(dataset,items)
	#print(itemsets[1],max_cand)
	print(dataset.count(['I1']))
	'''alphabets = ['a', 'b', 'c']

	for (a,b) in combinations(alphabets, 2):
	    print(a+b)'''

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

		if(len(L_freq_itemsets[i])==0):
			break


	print(C_candidate_itemsets,'\n',L_freq_itemsets)


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
