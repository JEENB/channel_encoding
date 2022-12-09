import numpy as np
from utils import *
from tabulate import tabulate

class Channel:
	def __init__(self, G, H) -> None:
		self.n = 4
		self.k = 2
		self.d = self.n - self.k
		self.G = G
		self.H = H
		self.codeword = get_codeword(self.G, code=generate_binary(self.k))
		self.std_arr = get_standard_array(n = self.n, codeword = self.codeword)
		# print("Codewords:", self.codeword)
		# print("Standard Array", self.std_arr)

		if self.G.shape != (self.n, self.k) or self.H.shape != (self.d, self.n):
			raise ValueError("Matrix shape mismatch")
		
		
	def encode(self, data:str) -> list:
		if len(data) != self.k:
			raise ValueError
		numpy_equiv_data = np.array(list(data), dtype=int)
		codeword = np.matmul(self.G, numpy_equiv_data)%2
		return list(codeword)

	def add_error(self, p:float, codeword) -> list:
		if p < 0 and p > 1:
			raise ValueError("Expected between 0 and 1")
		y_prime = []
		error = []
		for c in codeword:
			e = bsc(p)
			# print(e), print(c)
			y_p = np.bitwise_xor(c, e)
			y_prime.append(y_p)
			error.append(e)
		
		return y_prime, error

	def decode(self, y_prime:list) -> str:
		coset_synd = {} ## dict of coset leader and syndrome
		for arr in self.std_arr.values():
			coset_synd[arr[0]] = np.matmul(self.H,convert_str_to_numpy(arr[0]))%2
		syndrome = np.matmul(self.H, y_prime)%2
		coset_leader = get_key(coset_synd, syndrome)
		y = np.bitwise_or(y_prime, convert_str_to_numpy(coset_leader))
		return string_equiv_from_list(y[0:self.k])
		
def simulate(channel:Channel, n:int, p:float):
    X = generate_binary(2)
    word_error_count = 0
    ser = 0
    for i in range(n):
        x = string_equiv_from_list(random.choice(X))  ## randomly choose a 2 bit binary 

        codeword = channel.encode(x)
        y_prime, er = channel.add_error(p=p, codeword=codeword)
        x_prime = channel.decode(y_prime=y_prime)
                
        ## calculate ser
        for i in range(len(x_prime)):
            symbol_error_count = 0
            if x_prime[i] != x[i]:  
                symbol_error_count += 1
        ser += (symbol_error_count/len(x_prime))
		

        ## calculate wer
        if symbol_error_count/len(x_prime) > 0:
            word_error_count += 1
            
    # print(word_error_count, ser/n)
    return word_error_count/n, ser/n

def main():
	G = np.array([  [1,0],
                [0,1],
                [1,0],
                [1,1]
              ])

	H = np.array([  [1,0,1,0],
					[1,1,0,1]
				])

	c = Channel(G, H)

	num_simulations = [10, 100, 1000, 10000, 100000]
	output = []
	for i in num_simulations:
		wer, ser = simulate(channel = c, n = i, p = 0.3)
		output.append([i, wer, ser])
	print(tabulate(output, headers= ['Simulation', 'Wer', 'Ser'], tablefmt="pretty", numalign='center'))
	
if __name__ == '__main__':
	main()


