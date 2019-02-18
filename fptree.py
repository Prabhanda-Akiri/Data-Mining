import csv
import numpy as np
from itertools import chain
from itertools import combinations
valid_l=[]
def main():
	f_no=input('\nChoose the data file\n1. test_dataset_1.csv \n2. retail_dataset.csv \n')
	transactions=read_file(f_no)

	min_support=int(input('\nEnter minimum support:	'))
	min_confidence=int(input('\nEnter minimum confidence:	'))

	items=get_items(transactions)
	print(items)
	fp_tree,support_table=generate_fp_tree(items,transactions,min_support)
	#print_tree(fp_tree)
	association_rules=fp_tree_mining(fp_tree,support_table,min_confidence,min_support)

def print_tree(head):

	print(head.value)
	#print('children')
	for i in range(len(head.children)):

		print_tree(head.children[i])

def fp_tree_mining(fp_tree,support_table,min_confidence,min_support):

	mining_table=[]
	item_list=get_internals(fp_tree,None)
	item_list=list(set(item_list))
	print(item_list)

	for i in range(len(item_list)):
		print(item_list[i])
		temp=mining_items()
		temp.value=item_list[i] 
		mining_table.append(temp)
		del valid_l[:]
		get_paths(fp_tree,temp.value,[],-1)
		#print(valid_l)
		mining_table[i].conditional_pattern_base=valid_l
		#print(mining_table[i].conditional_pattern_base)
		mining_table[i].conditional_fp_tree=create_conditional_fp_tree(mining_table[i].conditional_pattern_base,min_support)
		print(mining_table[i].conditional_fp_tree)

		mining_table[i].frequent_patterns=generate_patterns(mining_table[i].conditional_fp_tree,item_list[i])
		print(mining_table[i].frequent_patterns)

		

def create_conditional_fp_tree(conditional_pattern_base,min_support):

	items=get_mining_items(conditional_pattern_base)
	#print(items)
	tree,table=generate_mining_fp_tree(items,conditional_pattern_base,min_support)
	branches=get_branches(tree,[],-1)

	return branches

def generate_patterns(branches,item_value):

	patterns=[]
	for i in range(len(branches)):
		for j in range(2,len(branches)+2):
			patterns+=list(combinations(branches[i]+[item_value],j))

	return patterns

def get_branches(head,l,index):

	if head.value!=None:
		l[index].append(head.value)
		for i in range(len(head.children)):
			l=get_branches(head.children[i],l,index)
	else:
		for i in range(len(head.children)):
			l.append([])
			index=len(l)-1
			l=get_branches(head.children[i],l,index)
	return l

def get_paths(head,value,l,index):
	
	#print(valid_l,l,head.value,value)

	if head.value==value:
		temp=[]
		for i in range(len(l[index])):
			temp.append(l[index][i])
		temp.append(head.count)
		valid_l.append(temp)
		l[index]=None
		return l
	if head.value!=None and head.value!=value and len(head.children)!=0:
		l[index].append(head.value)

	if len(head.children)==0:
		l[index]=None
		return l

	if head.value!=None:
		copy=[]
		for i in range(len(l[index])):
			copy.append(l[index][i])
	
	for i in range(len(head.children)):
		if head.value!=None:
			if i>0:
				l.append(copy)
				index=len(l)-1
			
			l =get_paths(head.children[i],value,l,index)
		else:
			l.append([])
			index=len(l)-1
			l=get_paths(head.children[i],value,l,index)

	return l

def get_internals(head,l):
	if l==None:
		l=[]
		for i in range(len(head.children)):
			l=get_internals(head.children[i],l)
	else:
		for i in range(len(head.children)):
			l.append(head.children[i].value)
			l=get_internals(head.children[i],l)
	return l

def generate_fp_tree(items,transactions,min_support):

	support_table=get_support_count(items,transactions,min_support)
	new_transactions=get_new_transactions(transactions,support_table)
	fp_tree=construct_fp_tree(support_table,new_transactions)

	return fp_tree,support_table

def generate_mining_fp_tree(items,transactions,min_support):

	support_table=get_mining_support_count(items,transactions,min_support)
	new_transactions=get_new_transactions(transactions,support_table)
	fp_tree=construct_fp_tree(support_table,new_transactions)

	return fp_tree,support_table

def construct_fp_tree(support_table,new_transactions):

	head=tree_node()

	for i in range(len(new_transactions)):
		current_state=head

		for j in range(len(new_transactions[i])):
			current_item=new_transactions[i][j]

			if current_item not in [ k.value for k in current_state.children]:
				temp=tree_node()
				temp.value=current_item
				temp.count=1
				current_state.children.append(temp)
				current_state=current_state.children[-1]

			else:
				k=[ k.value for k in current_state.children].index(current_item)
				current_state.children[k].count+=1
				current_state=current_state.children[k]

	return head

def get_new_transactions(transactions,support_table):

	new_transactions=[]

	for i in range(len(transactions)):
		l=[]
		for j in range(len(support_table)):
			if support_table[j][0] in transactions[i]:
				l.append(support_table[j][0])

		new_transactions.append(l)

	return new_transactions

def get_mining_support_count(items,transactions,min_support):

	no_items=len(items)
	count=[0 for i in range(no_items)]

	for i in range(len(transactions)):
		for j in range(len(transactions[i])-1):
			index=items.index(transactions[i][j])
			count[index]+=transactions[i][-1]

	table=[]
	for i in range(no_items):
		if count[i]>=min_support:
			l=[]
			l.append(items[i])
			l.append(count[i])
			table.append(l)
	table=sorted(table,key=lambda l:l[1], reverse=True)
	return table

def get_support_count(items,transactions,min_support):

	no_items=len(items)
	count=[0 for i in range(no_items)]

	for i in range(len(transactions)):
		for j in range(len(transactions[i])):
			index=items.index(transactions[i][j])
			count[index]+=1

	table=[]
	for i in range(no_items):
		if count[i]>=min_support:
			l=[]
			l.append(items[i])
			l.append(count[i])
			table.append(l)

	table=sorted(table,key=lambda l:l[1], reverse=True)
	return table

def get_items(dataset):
	#converting 2d list od input data into 1d list
	data=list(chain.from_iterable(dataset))

	#returning distinct items from 1d list
	return sorted(list(set(data)))

def get_mining_items(dataset):
	l=[]
	for i in range(len(dataset)):
		l+=dataset[i][:len(dataset[i])-1]
	return sorted(list(set(l)))

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


class tree_node:
	def __init__(self):
		self.value=None
		self.count=0
		self.children=[]

class mining_items:
	def __init__(self):
		self.item=None
		self.conditional_pattern_base=[]
		self.conditional_fp_tree=[]
		self.frequent_patterns=[]

if __name__ == '__main__':
	main()
