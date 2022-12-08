import math
from Pyro4 import expose


def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[i] < arr[l]:
        largest = l

    if r < n and arr[largest] < arr[r]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)

    for i in range(n//2, -1, -1):
        heapify(arr, n, i)

    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)


def merge(res, arr1, arr2):
    assert(len(res) == len(arr1) + len(arr2))

    i = j = k = 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            res[k] = arr1[i]
            i += 1
        else:
            res[k] = arr2[j]
            j += 1
        k += 1

    while i < len(arr1):
        res[k] = arr1[i]
        i += 1
        k += 1

    while j < len(arr2):
        res[k] = arr2[j]
        j += 1
        k += 1


class Solver:

    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        work_count = len(self.workers)

        input_list = self.read_input()

        chunks = self.get_chunks(input_list, work_count)

        mapped = []
        for i in xrange(0, work_count):
            mapped.append(self.workers[i].mymap(chunks[i]))

        reduced = self.myreduce(mapped)

        self.write_output(reduced)

    @staticmethod
    @expose
    def myreduce(mapped):
        mapped_lists = []

        for x in mapped:
            mapped_lists.append(x.value)

        while len(mapped_lists) > 1:
            tmp = []

            for i in xrange(0, len(mapped_lists), 2):
                if i != len(mapped_lists) - 1:
                    new_list = [None] * (len(mapped_lists[i]) + len(mapped_lists[i+1]))
                    merge(new_list, mapped_lists[i], mapped_lists[i+1])
                    tmp.append(new_list)
                else:
                    new_list = [None] * (len(mapped_lists[i]) + len(tmp[-1]))
                    merge(new_list, mapped_lists[i], tmp[-1])
                    tmp[-1] = new_list

            mapped_lists = tmp

        return mapped_lists[0]

    @staticmethod
    def get_chunks(lst, n):
        res = []

        d, r = divmod(len(lst), n)
        for i in range(n):
            si = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
            res.append(lst[si:si+(d+1 if i < r else d)])

        return res

    def read_input(self):
        res = []
        with open(self.input_file_name, 'r') as in_file:
            for line in in_file:
                res.append(int(line))
        return res

    def write_output(self, out_list):
        with open(self.output_file_name, 'w') as in_file:
            for n in out_list:
                in_file.write(str(n) + "\n")

    @staticmethod
    @expose
    def mymap(chunk):
        heap_sort(chunk)
        return chunk
