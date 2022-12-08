from Pyro4 import expose
from os import stat
import random
from heapq import merge

class Solver:

    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        n = self.read_input()
        step = n / len(self.workers)
        mapped = []
        lastElementI = len(self.workers) - 1

        for i in range(0, lastElementI):
            mapped.append(self.workers[i].mymap(i * step, i * step + step))
        mapped.append(self.workers[lastElementI].mymap(lastElementI * step, n))
        reduced = self.myreduce(mapped)
        self.write_output(reduced)


    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    @staticmethod
    def power(a, b, n):
        if b == 0:
            return 1
        if b % 2 == 0:
            return Solver.power(a * a % n, b // 2, n)
        else:
            return a * Solver.power(a * a % n, b // 2, n) % n
 
    
    @staticmethod
    def primeFermat(n, iter):
        if n < 4:
            return n == 2 or n == 3
        for i in range(iter):
            a = 2 + random.randint(0, n - 3)
            if Solver.power(a, n - 1, n) != 1:
                return False
        return True
    
    @staticmethod
    @expose
    def mymap(a, b):
        res_arr = []
        for n in range(a,b):
            if (Solver.primeFermat(n, 50)):
                res_arr.append(n)
        return res_arr
 
    @staticmethod
    def myreduce(mapped):
        result = []
        wnum = len(mapped)
        result = mapped[0].value
        for i in range(1, wnum):
            result = list(merge(result, list(mapped[i].value)))
        return result
    

    def write_output(self, output):
        f = open(self.output_file_name, 'w')

        for a in output:
            f.write(str([a]) + "\n")
            
        f.close()
