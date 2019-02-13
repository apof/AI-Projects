import sys
import time
import csp

def add(numbers):
	sum = 0
	for n in numbers:
		sum += n
	return sum
	
class Kakuro(csp.CSP):

	def kakuro_constraints(self, A, a, B, b):
	
		if (A[1] == B[1] or A[2] == B[2]):
			flag = 0
			for l in self.lines:
				if ((A in l[0]) and (B in l[0])):
					flag = 1
			if a == b and flag == 1:
				return False

		numbers = [ ]
		NoValue = 0

		for line in self.lines:
		
			variables = line[0]
			result  = line[1]

			if A in variables and B in variables:

				if len(variables) == 2:
					sum  = add([a,b])
					if (sum == result):
						return True
					else:
						return False
				else:
					for var in variables:
						if var == A:
							numbers.append(a)
						elif var == B:
							numbers.append(b)
						else:
							if self.curr_domains == None or len(self.curr_domains[var]) > 1:
								NoValue += 1
							elif len(self.curr_domains[var]) == 1:
								numbers.append(*self.curr_domains[var])
					if NoValue == 0:
						sum = add(numbers)
						if (sum == result):
							return True
						else:
							return False
					else:
						sum = add(numbers)
						if (sum <= result):
							return True
						else:
							return False
		return True

	def __init__(self, rows, cols, lines,black_vars):

		self.rows = rows
		self.cols = cols
		self.lines = lines
		self.black_vars = black_vars

		variables = [ ]
		domains = { }
		neighbors = { }

		for i in range(rows):
			for j in range(cols):
			
				var = "X%d%d" % (i,j)
				if(var not in black_vars):
				
					variables.append(var)	
					domains[var] = [n + 1 for n in range(9)]
					neighbors[var] = [ ]

					for row in range(rows):
						for col in range(cols):

							neighbor = "X%d%d" % (row,col)
						
							if neighbor != var and (i == row or j == col) and (neighbor not in black_vars):
								neighbors[var].append(neighbor)

		csp.CSP.__init__(self, variables, domains, neighbors, self.kakuro_constraints)



if __name__ == '__main__':

	if len(sys.argv) != 2:
		print("Usage: kakuro.py <input_file>")
	else:
		inputFile = open(sys.argv[1], 'r')

		data = inputFile.readlines()

		inputFile.close()

		rows = int(data[0])
		columns = int(data[1])

		lines = [ ]

		for i in range(2, len(data)):

			vars = []
			substrings = data[i].split()
			substrings[0] = substrings[0][2:-2]
			points = substrings[0].split("),(")

			for point in points:
				var = "X%d%d" % (int(point[0]), int(point[2]))
				vars.append(var)

			add_res = int(substrings[1])
			
			line = [vars,add_res]

			lines.append(line)
			
		black_vars = []
		
		for i in range(rows):
			for j in range(columns):
				v = "X%d%d" % (i,j)
				flag = 0
				for l in lines:
					if v in l[0]:
						flag = 1
				if (flag == 0):
					black_vars.append(v)
					
		print("-->BT")
		BT = Kakuro(rows,columns,lines,black_vars)
		start = int(round(time.time()*1000))
		result_BT = csp.backtracking_search(BT)
		end = int(round(time.time()*1000))
		print("Solved with BT in %d mseconds with %d assignments.\n" % (end - start, BT.nassigns))

		print("-->FC")
		FC = Kakuro(rows,columns,lines,black_vars)
		start = int(round(time.time()*1000))
		result_FC = csp.backtracking_search(FC, inference=csp.forward_checking)
		end = int(round(time.time()*1000))
		print("Solved with FC in %d mseconds with %d assignments.\n" % (end - start, FC.nassigns))

		print("-->FC+MRV")
		FCMRV = Kakuro(rows,columns,lines,black_vars)
		start = int(round(time.time()*1000))
		result_FCMRV = csp.backtracking_search(FCMRV, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
		end = int(round(time.time()*1000))
		print("Solved with FC+MRV in %d mseconds with %d assignments.\n" % (end - start, FCMRV.nassigns))

		print("-->MAC")
		MAC = Kakuro(rows,columns,lines,black_vars)
		start = int(round(time.time()*1000))
		result_MAC = csp.backtracking_search(MAC, inference=csp.mac)
		end = int(round(time.time()*1000))
		print("Solved with MAC in %d mseconds with %d assignments.\n" % (end - start, MAC.nassigns))

		
		print("\nSollution (--> Variable = Values):\n")
		for i in range(rows):
			for j in range(columns):
				if (result_BT.items()!=None):
					for (var, val) in result_BT.items():
						if var == "X%d%d" % (i, j):
							print("%s = %d" % (var, val), end = "  ")
			print("")