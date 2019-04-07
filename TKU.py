import numpy as np
import bisect as bi
from random import randint

class transaction:
	def __init__(self):
		self.items=[]
		self.total_utility=0
		self.each_utility=[]
		#self.transaction_id=0
	def extract_elements(self,each_transaction):
		S=each_transaction.split(":")
		S[0]=S[0].split(" ")
		S[2]=S[2].split(" ")

		for each_item in S[0]:
			self.items.append(int(each_item))

		self.total_utility=int(S[1])

		for each_util in S[2]:
			self.each_utility.append(int(each_util))

class Itemset():
	def __init__(self):
		self.itemset=None
		self.support_count=0
		self.transactions=None
		self.MIU=0
		self.EU=0
		self.ESTU=0
		self.TWU=0
		self.MAU=0

class Header_Table_Entry():
	def __init__(self):
		self.item=0
		self.TWU=0
		self.link=None

class UP_Tree_Node():
	def __init__(self):
		self.item_id=0
		self.count=0
		self.node_utility=0
		self.child=[]
		self.hlink=None
		self.transaction_ids=[]
class UP_TREE():
	def __init__(self):
		self.root=UP_Tree_Node()

class TKU_algorithm:

	def __init__(self,K):

		self.K=K
		self.no_items=None
		self.all_items=[]
		self.Transaction_objects=[]
		self.Pre_Evaluation_matrix=[]
		self.min_util_border=0
		self.Header_Table=[]
		self.TWU_dict={}
		self.Sorted_transactions=[]
		self.UP_Tree=UP_TREE()
		self.node_utilities=[]
		self.transaction_utilities_eachItem=None
		self.min_utility_items=[]
		self.max_utility_items=[]
		self.PKHUIs=[]
		self.Itemsets=[]
		self.Top_k_itemsets=[]
		self.Top_k_MIU=[]

	def load_dataset(self):

		f=open("foodmart_items.txt","r")
		for each_item in f:
			self.all_items.append(int(each_item))

		self.no_items=len(self.all_items)
		
		#Strategy 2
		self.Pre_Evaluation_matrix=[[0 for i in range(self.no_items)] for j in range(self.no_items)]

		f=open("foodmart_utility.txt","r")
		total_transactions=sum([1 for item in f])
		print(total_transactions)
		self.transaction_utilities_eachItem=[[None for i in range(total_transactions)]for j in range(self.no_items)]

		c=0
		print('hi')
		with open('foodmart_utility.txt','r') as f:
			for item in f:
				#print('hi')
				temp=transaction()
				temp.extract_elements(item)
				self.Transaction_objects.append(temp)
				#print(temp.total_utility)
				for i in range(len(temp.items)):
					index_i=self.all_items.index(temp.items[i])
					self.transaction_utilities_eachItem[index_i][c]=temp.each_utility[i]
					for j in range(len(temp.items)):
						self.Pre_Evaluation_matrix[temp.items[i]-1][temp.items[j]-1]+=(temp.each_utility[i]+temp.each_utility[j])

				c+=1
				#self.all_items=self.all_items+temp.items
		
		temp_pre_eval=np.array(self.Pre_Evaluation_matrix)
		temp_pre_eval=temp_pre_eval.flatten()
		temp_pre_eval.sort()
		min_util_border_temp=temp_pre_eval[-(self.K)]

		if self.min_util_border<min_util_border_temp:
			self.min_util_border=min_util_border_temp

		print(self.min_util_border)
		#self.all_items=list(set(self.all_items))
		# with open('foodmart_items.txt', 'w') as f:
		#     for item in self.all_items:
		#         f.write("%s\n" % item)

	def header_table_construction(self):
		for each_item in self.all_items:
			table_entry=Header_Table_Entry()
			table_entry.item=each_item

			for each_transaction in self.Transaction_objects:
				if each_item in each_transaction.items:
					table_entry.TWU= table_entry.TWU + each_transaction.total_utility

			self.TWU_dict[table_entry.item]=table_entry.TWU
			self.Header_Table.append(table_entry)

		Header_Table.sort(key=lambda x: x.TWU, reverse=True)

	def Construct_UP_tree(self):
		for each_transaction in self.Transaction_objects:
			sorted_dict={}
			Tr_dash=transaction()
			items_in_transaction=each_transaction.items
			for each_item in items_in_transaction:
				sorted_dict[each_item]=TWU_dict[each_item]

			y=dict(sorted(sorted_dict.items(), key=lambda x: x[1],reverse=True))
			Sorted_items=list(y.keys())
			Sorted_utility=[]

			#Sorted_transaction_items.append(Tr_dash)
			for each in Sorted_items:
				indx=each_transaction.items.index(each)
				Sorted_utility.append(each_transaction.each_utility[indx])
			Tr_dash.items=Sorted_items
			Tr_dash.each_utility=Sorted_utility
			Tr_dash.total_utility=each_transaction.total_utility
			Tr_dash.transaction_id=each_transaction.transaction_id

			self.Insert_Reorganized_transaction(self.UP_Tree.root,Sorted_items[0],Tr_dash)

	def Insert_Reorganized_transaction(self,N,Ij,Z):
		j=Z.items.index(Ij)
		if j<=len(Tr_dash.items):

			temp_l=[eachChN.item for eachChN in N.child]

			if Ij in temp_l:
				k=temp_l.index(Ij)
				N.child[k].count+=1
				N.child[k].transaction_ids.append(Z.transaction_id)
				ChN=N.child[k]
			else:
				ChN=UP_Tree_Node()
				N.child.append(ChN)
				ChN.item=Ij
				ChN.count=1
				ChN.node_utility=0

			RTU_Tr=self.Cal_RTU(Z)
			
			sigma_EU=0
			for i in range(j+1,len(Z.items)):

				#EU_item=Cal_EU(Z.items[i],Z)
				sigma_EU+=Z.each_utility[i]

			ChN.node_utility += RTU_Tr - sigma_EU
			bi.insort(self.node_utilities,ChN.node_utility)

			#strategy 3
			if self.get_count_UP_tree(self.UP_Tree.root,1)>self.K:
				if self.min_util_border<self.node_utilities[k]:
					self.min_util_border=self.node_utilities[k]

			return Insert_Reorganized_transaction(ChN,Z[j+1],Z)

	def Cal_RTU(self,Tr):
		return Tr.total_utility

	def get_count_UP_tree(self,node,count):

		for child in node.child:
			count+=self.get_count(child,1)
		return count

	def get_min_utility_items(self):

		for index in range(self.no_items):
			self.min_utility_items[index]=min([x for x in self.transaction_utilities_eachItem[index] if x!=None])

	def get_max_utility_items(self):

		for index in range(self.no_items):
			self.max_utility_items[index]=max([x for x in self.transaction_utilities_eachItem[index] if x!=None])

	def generate_ESTU(self,iset):

		#for iset in self.Itemsets:			
		#index_j=self.Itemsets.index(iset)
		sum_miu=0
		sum_mau=0
		sum_eu=0

		for i in iset.itemset:

			index_i=self.all_items.index(i)
			#generate MIU
			sum_miu+=self.min_utility_items[index_i]
			#generate EU
			sum_eu+=sum(self.transaction_utilities_eachItem[index_i])
			#generate MAU
			sum_mau+=self.max_utility_items[index_i]

		#genrate TWU
		iset.TWU=sum([self.Transaction_objects[i].total_utility for i in iset.transactions])
		iset.MIU=sum_miu*iset.support_count
		iset.EU=sum_eu*iset.support_count
		iset.MAU=sum_mau*iset.support_count

		#generate ESTU
		while True:
			estu=randint(iset.EU,iset.TWU)
			if iset.eu<=min(estu,iset.mau):
				break

		iset.ESTU=estu 		
		return iset

	def check_pkhui(self,iset):

		if(iset.ESTU>=self.min_util_border) and (iset.MAU>=min_util_border):
			self.Top_k_itemsets.append(iset)
			bi.insort(self.Top_k_MIU,iset.MIU)

			#strategy 4
			if iset.MIU>=self.min_util_border:
				if len(self.Top_k_MIU)>self.K:
					if self.Top_k_MIU[k-1]>self.min_util_border:
						self.min_util_border=self.Top_k_MIU[k-1]
		else:
			return 'Not a PKHUI'

	def apply_TKU(self):

		for iter_i in range(len(self.Itemsets)):
			self.Itemsets[iter_i]=self.generate_ESTU(self.Itemsets[iter_i])


		#Strategy 5---------
		self.Itemsets.sort(key=lambda x: x.ESTU, reverse=True)

		for iter_i in range(len(self.Itemsets)):

			return_val=self.check_pkhui(self.Itemsets[iter_i])
			if return_val=='Not a PKHUI':
				break
		#-------------------

	def generate_pkhuis(self):
		itmsets=[]
		root_of_up=self.UP_TREE.root
		paths=[]
		path_for_each_leaf=[]
		path_for_each_leaf = find_path(root_of_up,path_for_each_leaf,0)
		#path_for_each_leaf=prune(path_for_each_leaf)
		#new_itemset=itemset_generation(path_for_each_leaf)
		paths.append(path_for_each_leaf)

	def find_path(self,rootNode,path,pathLen):
		all_leafs_path=[]
		if rootNode is None:
			return
		if (len(path)>pathLen):
			path[pathLen]=rootNode
		else:
			path.append(rootNode)

		pathLen=pathLen+1

		if len(rootNode.child)==0:
			print("path:",path)
			pruned_path=prune(path)
			generate_itemsets(path)
		else:
			for each_child in rootNode.child:
				find_path(each_child,path,pathLen)

	def prune(self,path):
		length=len(path)
		for j in range(length-1,0,-1):
			temp=path[j]
			if temp.count<min_util_border:
				to_be_rem=j
		path=path[:to_be_rem]

	def generate_itemsets(self,path_list):

		for L in range(2, len(path_list)+1):
			print(itertools.combinations(path_list, L))
			for subset in itertools.combinations(path_list, L):
				if len(subset)>1:
					print(subset)
					all_items=[e.itemset for e in self.Itemsets]
					if subset in all_items:
						index_i=all_items.index(subset)
						self.Itemsets[index_i]+=1
					else:
						temp=Itemset()
						temp.itemset=subset
						temp.support_count=1
						self.Itemsets.append(temp)

tku=TKU_algorithm(100)
tku.load_dataset()
