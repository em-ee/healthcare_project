#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random as rand
import matplotlib.pyplot as plt
import time
import pandas as pd


def myHealthcare_pd(n):

    '''This function uses a dictionary and Pandas to create the simulated data
    as per the specifications.'''

    rand.seed(404)

    d = {'ts' : [i+1000 for i in range(n)],
         'temp' : [rand.randint(36, 39) for i in range(n)],
         'hr' : [rand.randint(55,100) for i in range(n)],
         'pulse' : [rand.randint(55, 100) for i in range(n)],
         'bloodpr' : [rand.randint(120,121) for i in range(n)],
         'resrate' : [rand.randint(11,17) for i in range(n)],
         'oxsat' : [rand.randint(93,100) for i in range(n)],
         'ph' : [round(rand.uniform(7.1, 7.6),1) for i in range(n)]}

    vitalsigns_pd = pd.DataFrame(d)

    return vitalsigns_pd



def myHealthcare(n):

    rand.seed(404)

    '''This function uses list comprehensions and zip() to create the simulated
    data as per the specifications. Data is joined together as a 2D array, giving
    a set of observations for each `ts`.'''

    ts = [i+1000 for i in range(n)]
    temp = [rand.randint(36, 39) for i in range(n)]
    hr = [rand.randint(55,100) for i in range(n)]
    pulse = [rand.randint(55, 100) for i in range(n)]
    bloodpr = [rand.randint(120,121) for i in range(n)]
    resrate = [rand.randint(11,17) for i in range(n)]
    oxsat = [rand.randint(93,100) for i in range(n)]
    ph = [round(rand.uniform(7.1, 7.6),1) for i in range(n)]

    vitalsigns = [[a,b,c,d,e,f,g,h] for a,b,c,d,e,f,g,h
                  in zip(ts, temp, hr, pulse, bloodpr, resrate, oxsat, ph)]

    return vitalsigns



def abnormalSignAnalytics(data, sample, sign = ['bloodpr', 'pulse']):

    '''Takes data generated by myHealthcare(), a sample size and the
    string corresponding to which vital sign abnormal values should be
    returned for.'''

    rand.seed(404)

    # create a list of random IDs to sample from:

    ids = [x[0] for x in data]

    sample_ids = rand.sample(ids, sample)

    # create a subset of original data based on the subset sample_ids:
    vitalsigns_subset = [x for x in data if x[0] in sample_ids]

    # return the abnormal values for blood pressure or pulse:
    if sign == "bloodpr":

        bp = [(x[0], x[4]) for x in vitalsigns_subset if x[4] > 120]

        count = len(bp)

        return "abnormal blood pressure cases: " + str(count) + ": " + str(bp)

    elif sign == "pulse":

        pul_under = [(x[0], x[3]) for x in vitalsigns_subset if x[3] < 60]
        pul_over = [(x[0], x[3]) for x in vitalsigns_subset if x[3] > 99]

        count = len(pul_under)+len(pul_over)

        return "abnormal pulse rate cases: ", count, pul_under, pul_over



def frequencyAnalytics(data, sample, sign = ['ts', 'temp', 'hr', 'pulse', 'bloodpr', 'resrate', 'oxsat', 'ph']):

    '''Takes data generated by myHealthcare(), a sample size and the
    string corresponding to which vital sign frequencies should be
    returned for.'''

    rand.seed(404)

    d = {'ts':0, 'temp':1, 'hr':2, 'pulse':3, 'bloodpr':4, 'resrate':5, 'oxsat':6, 'ph':7}

    col = d.get(sign)

    # create a list of random IDs to sample from:

    ids = [x[0] for x in data]

    sample_ids = rand.sample(ids, sample)

    # create a subset of original data based on the subset sample_ids:

    subset = [x[col] for x in data if x[0] in sample_ids]

    # return frequency values for each pulse rate:

    freq = {}

    for i in subset:

        freq[i] = freq.get(i, 0)+1

    return [(v, f) for v, f in freq.items()]



def healthAnalyzer(data, value, sign = ['ts', 'temp', 'hr', 'pulse', 'bloodpr', 'resrate', 'oxsat', 'ph'], searchtype = ['b', 'l']):

    '''Takes data generated by myHealthcare(), a value to look for,
    which vital sign to search in, and which search algorithm to use
    (b for binary, l for linear).'''

    rand.seed(404)

    # create a dictionary to assign column index number to measurement:

    d = {'ts':0, 'temp':1, 'hr':2, 'pulse':3, 'bloodpr':4, 'resrate':5, 'oxsat':6, 'ph':7}

    col = d.get(sign)

    if searchtype == 'l':

        # linear search - return all elements where value of measurement is matched:

        pr = [x for x in data if x[d.get(sign)] == value]

        if pr == []:

            return "Value not found"

        else:

            return pr

    elif searchtype == 'b':

        # Binary search: sort the data first by the column we will search in

        data_sorted = sorted(data, key =  lambda x: x[col])

        l = 0
        r = len(data_sorted)-1
        results = []

        # check whether the value is in range

        if (data_sorted[l][col] > value or data_sorted[r][col] < value):

            return "Value not in data: value out of range."

        # check whether the value is last or first in the sorted list

        elif data_sorted[l][col] == value:

            while data_sorted[l][col] == value:

                if l > len(data_sorted):

                    break

                else:

                    results.append(data_sorted[l])

                    l = l + 1

        elif data_sorted[r][col] == value:

            while data_sorted[r][col] == value:

                if r < len(data_sorted)-1:

                    break

                else:

                    results.append(data_sorted[r])

                    r = r - 1

        # Binary search for the value

        else:

            l = 0
            r = len(data_sorted)-1
            results = []

            mid = int(l + (r - l) / 2)

            while data_sorted[mid][col] != value:

                if l==r:

                    return "Value not in data: value not found."

                if data_sorted[mid][col] < value:

                    while (data_sorted[mid][col] < value and l < r):

                        l = mid+1

                        mid = int(l + (r - l) / 2)

                elif (data_sorted[mid][col] > value and r > l):

                    while data_sorted[mid][col] > value:

                        r = mid-1

                        mid = int(l + (r - l) / 2)

            # When found, find the first occurrence of the value

            while (data_sorted[mid][col] == value and mid > -1):

                mid = mid - 1

            # Then append all subsequent rows where the value appears.

            while (data_sorted[mid+1][col] == value and mid < len(data_sorted)):

                results.append(data_sorted[mid+1])

                mid = mid + 1


        return results



def benchmarkingMyHealthcare(lst):

    '''Takes a list of number of rows of data to produce and benchmarks.'''

    rand.seed(404)

    times = []

    for i in lst:

        start = time.time()

        myHealthcare(i)

        end = time.time()

        times.append(end-start)

    return times



def benchmarkingMyHealthcare_pd(lst):

    '''Takes a list of number of rows of data to produce and benchmarks.'''

    rand.seed(404)

    times = []

    for i in lst:

        start = time.time()

        myHealthcare_pd(i)

        end = time.time()

        times.append(end-start)

    return times



def benchmarkingHealthAnalyzer(data, value, sign, searchtype):

    '''Takes the same input values as healthAnalyzer() and benchmarks the
    search algorithm.'''

    rand.seed(404)

    times = []

    for i in searchtype:

        start = time.time()

        healthAnalyzer(data, value, sign, i)

        end = time.time()

        times.append(end-start)

    return times

##############################################################################

# generating dataset and calling functions for report:

data = myHealthcare(1000)

abnormal = abnormalSignAnalytics(data, 50, 'pulse')

freq = frequencyAnalytics(data, 50, 'pulse')

health = healthAnalyzer(data, 56, 'pulse', 'b')

timingsMyHealthcare = benchmarkingMyHealthcare([1000, 2500, 5000, 7500,10000])
timingsMyHealthcare2 = benchmarkingMyHealthcare_pd([1000, 2500, 5000, 7500,10000])
timingsHealthAnalyzer = benchmarkingHealthAnalyzer(data, 120, 'bloodpr', ['b','l'])
timingsHealthAnalyzer2 = benchmarkingHealthAnalyzer(data, 56, 'pulse', ['b','l'])

data_bm = myHealthcare(10000)
timingsHealthAnalyzer3 = benchmarkingHealthAnalyzer(data_bm, 56, 'pulse', ['b','l'])

# plots:

plt.scatter([x[0] for x in abnormal[2]], [x[1] for x in abnormal[2]], label = 'Low')
plt.scatter([x[0] for x in abnormal[3]], [x[1] for x in abnormal[3]], label = 'High')
plt.xlabel('ID number')
plt.ylabel('Pulse rate')
plt.title('A sample of abnormal pulse rates')
plt.legend()
plt.show()

plt.bar([x[0] for x in freq], [x[1] for x in freq])
plt.xlabel('Pulse rate')
plt.ylabel('Frequency')
plt.title('A sample of pulse rates and their frequencies')
plt.show()

plt.scatter([int(x[3]) for x in health], [int(x[2]) for x in health])
plt.xticks(range(50,60))
plt.xlabel('Pulse rate')
plt.ylabel('Heart rate')
plt.title('Heart rates of individuals with a pulse rate of 56')
plt.show()

plt.plot([1000, 2500, 5000, 7500,10000], timingsMyHealthcare, marker = 'x')
plt.xticks([1000, 2500, 5000, 7500,10000])
plt.ylim(0.00, 0.20)
plt.xlabel('Number of records generated')
plt.ylabel('Time elapsed (seconds)')
plt.title('Benchmarking myHealthcare(n) with a range of n')
plt.show()

plt.plot([1000, 2500, 5000, 7500,10000], timingsMyHealthcare2, marker = 'x')
plt.xticks([1000, 2500, 5000, 7500,10000])
plt.ylim(0.00, 0.20)
plt.xlabel('Number of records generated')
plt.ylabel('Time elapsed (seconds)')
plt.title('Benchmarking myHealthcare_pd(n) with a range of n')
plt.show()

plt.plot(['b', 'l'], timingsHealthAnalyzer, marker = 'x')
plt.xticks(['b', 'l'])
plt.ylim(0.000000, 0.001)
plt.xlabel('Type of search')
plt.ylabel('Time elapsed (seconds)')
plt.title('Benchmarking healthAnalyzer for binary and linear search: bloodpr of 120')
plt.show()

plt.plot(['b', 'l'], timingsHealthAnalyzer2, marker = 'x')
plt.xticks(['b', 'l'])
plt.ylim(0.000000, 0.001)
plt.xlabel('Type of search')
plt.ylabel('Time elapsed (seconds)')
plt.title('Benchmarking healthAnalyzer for binary and linear search: pulse of 56')
plt.show()

plt.plot(['b', 'l'], timingsHealthAnalyzer3, marker = 'x')
plt.xticks(['b', 'l'])
plt.ylim(0.000, 0.01)
plt.xlabel('Type of search')
plt.ylabel('Time elapsed (seconds)')
plt.title('Benchmarking healthAnalyzer for binary and linear search: larger dataset')
plt.show()
