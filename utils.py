import random
import numpy as np
import math

def bsc(p):
	# rand = random.uniform(0,1)
	# if rand < p:
	# 	return 1
	# else:
	# 	return 0

	return random.choices([0,1],weights=[1-p, p], k = 4)


def string_equiv(numpy_array):
	'''
	takes list of numpy array list and returns a list of strings
	 '''

	str_equiv = []
	for arr in numpy_array:
		temp = ''
		for i in arr:
			temp += str(i)
		str_equiv.append(temp)
	return str_equiv

def string_equiv_from_list(arr) -> str:
	''' takes a list of bit strings (single) and returns the string'''
	temp = ''
	for a in arr:
		temp += str(a)
	return temp


def convert_str_to_numpy(err):
 	return np.array(list(err), dtype= np.int32)

def generate_binary(n):
  # 2^(n-1)  2^n - 1 inclusive
  bin_arr = range(0, int(math.pow(2,n)))
  bin_arr = [bin(i)[2:] for i in bin_arr]

  # Prepending 0's to binary strings
  max_len = len(max(bin_arr, key=len))
  bin_arr = [np.array(list(i.zfill(max_len)), dtype=np.int32) for i in bin_arr]

  return bin_arr


# # Python code to sort a list of tuples 
# def last(n):
#     return n[m]  
   
# # function to sort the tuple   
# def sort(tuples):
  
#     # We pass used defined function last
#     # as a parameter. 
#     return sorted(tuples, key = last)
# m = 1
def get_codeword(G, code):
	codeword = []
	for msg in code:
		codeword.append((np.matmul(G, msg)%2))
	return codeword

def get_weight(string):
	w = 0
	for i in string:
		if i == '1':
			w += 1
	return w


def sort(array):
	sorted_array = []
	s = []
	for i in array:
		s.append((get_weight(i), i))
	sor = sorted(s, key = lambda x: x[0])
	for j in sor:
		sorted_array.append(j[1])

	# print(sorted_array)
	return sorted_array
	
def get_standard_array(n, codeword):
	all_possible_error = generate_binary(n)
	str_all_possible_error = string_equiv(all_possible_error)

	str_codeword = string_equiv(codeword)
	# print(str_codeword)

	## remove codewords from all_possible_errors
	for ce in codeword:
		str_all_possible_error.remove(string_equiv_from_list(ce))

	coset = {}
	coset[str_codeword[0]] = str_codeword

	min_idx_list = []

	while len(str_all_possible_error) > 0:
		u_i = random.sample(str_all_possible_error, k = 1)[0]  #str
		u_i_np = np.array(list(u_i), dtype= np.int32)
		coset_members = []
		for word in codeword:
			# print(word.shape)
			xor =  u_i_np ^ word #numpy list
			# print(xor)
			coset_members.append(string_equiv_from_list(xor))
			str_all_possible_error.remove(string_equiv_from_list(xor))
		# print("Sorted", sort(coset_members))
			
		coset[u_i] = sort(coset_members)
	# print(coset)
	return coset

# function to return key for any value
def get_key(my_dict,val) -> str:
    for key, value in my_dict.items():
        # print(string_equiv_from_list(val))
        # print(string_equiv_from_list(value))
        if string_equiv_from_list(val) == string_equiv_from_list(value):
            return key
 
    return "key doesn't exist"