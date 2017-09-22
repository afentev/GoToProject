from math import fabs
from random import choices

import pandas as pd
from numpy import zeros, array

import Data

nucleotides = ['A', 'T', 'G', 'C']


def local_maximum(s1, s2):
    matrix = zeros((len(s1) + 1, len(s2) + 1))
    directions = [[0 for _ in range(len(s2) + 1)] for _ in range(len(s1) + 1)]
    matrix[0], directions[0] = [-i for i in range(len(s2) + 1)], [(0, i - 1) for i in range(len(s2) + 1)]
    for row_index in range(len(s1) + 1):
        matrix[row_index][0] = -row_index
        directions[row_index][0] = (row_index - 1, 0)
    directions[0][0] = None

    maximum = (0, (0, 0))
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            maximum_iter = max([matrix[i - 1][j - 1] + 1 if s1[i - 1] == s2[j - 1] else matrix[i - 1][j - 1] - 1,
                                matrix[i - 1][j] - 1, matrix[i][j - 1] - 1])
            if maximum_iter < 0:
                maximum_iter = 0
            matrix[i][j] = maximum_iter
            if maximum_iter > maximum[0]:
                maximum = (maximum_iter, (i, j))

            if matrix[i - 1][j] - 1 == maximum_iter:
                directions[i][j] = (i - 1, j)
            elif matrix[i][j - 1] - 1 == maximum_iter:
                directions[i][j] = (i, j - 1)
            elif matrix[i - 1][j - 1] + 1 == maximum_iter if s1[i - 1] == s2[j - 1]\
                    else matrix[i - 1][j - 1] - 1 == maximum_iter:
                directions[i][j] = (i - 1, j - 1)

    string1, string2 = '', ''
    index = maximum[1]

    while index != 0:
        new_index = directions[index[0]][index[1]]
        if new_index == 0 or new_index is None:
            break
        if index[0] > new_index[0] and index[1] == new_index[1]:
            string1 += s1[index[0] - 1]
            string2 += '-'
        elif index[1] > new_index[1] and index[0] == new_index[0]:
            string2 += s2[index[1] - 1]
            string1 += '-'
        else:
            string1 += s1[index[0] - 1]
            string2 += s2[index[1] - 1]
        index = new_index

    return string1[::-1]


def get_nucleotide_sequence(alphabet, k):
    return ''.join(choices(alphabet, k=k))


def binary_search(sequence, element):
    start = 0
    end = len(sequence) - 1
    middle = int(end / 2)
    while element not in sequence[middle] and start < end:
        if element > max(sequence[middle]):
            start = middle + 1
        else:
            end = middle - 1
        middle = int((start + end) / 2)
    if start > end:
        return None
    else:
        return middle


def connect_exons(gtf: str = 'exons.gtf', sam: str = 'm1.sam'):
    names = {}
    coverage = {}
    borders = {}
    with open('C:\\Users\\kiril\\PycharmProjects\\GoToProjects\\{}'.format(gtf), 'r') as file:
        line = '.'
        while line:
            line = file.readline().replace('\n', '').strip().split()
            if line:
                name = line[9][1:-2]
                if name in names.keys():
                    names[name].append(line)
                else:
                    names[name] = [line]
                coverage[name] = {}
                borders[range(int(line[3]), int(line[4]) + 1)] = [(line[0], name)]

    keys = list(borders.keys())

    with open('C:\\Users\\kiril\\PycharmProjects\\GoToProjects\\{}'.format(sam), 'r') as file:
        line = '.'
        while line:
            line = file.readline().replace('\n', '').strip().split()
            if line:
                bar, umi = line[-2], line[-1]
                position = int(line[3]) + int(line[4])
                result = binary_search(keys, position)
                if result is not None:
                    if bar in coverage[borders[keys[result]][0][1]].keys():
                        coverage[borders[keys[result]][0][1]][bar] += 1
                    else:
                        coverage[borders[keys[result]][0][1]][bar] = 1
    return coverage


def create_matrix(dictionary):
    return pd.DataFrame(dictionary).fillna(0)

# matrix = create_matrix(Data.data).T
# normalize_matrix = matrix / matrix.mean()
# results = {}
#
# labels_dict = {}
# gens = []
# with open('large_cells.txt', 'r') as labels:
#     lines = list(map(lambda y: y.replace('\n', '').strip().split(), labels.readlines()))
#     for x in lines:
#         gens.append('CB:Z:' + x[0])
#         labels_dict['CB:Z:' + x[0]] = x[1]
# print(labels_dict)
#
# for gen in normalize_matrix.iterrows():
#     results[gen[:-1]] = 0
#     data = list(map(lambda y: y.split(), str(gen[1]).split('\n')))[:-1]
#     monocytes_amount_count = [0, 0]
#     macrophages_amount_count = [0, 0]
#     for index in range(1000):
#         for a in data:
#             if labels_dict[a[0]] == 'macrophages':
#                 macrophages_amount_count[0] += float(a[1])
#                 macrophages_amount_count[1] += 1
#             else:
#                 monocytes_amount_count[0] += float(a[1])
#                 monocytes_amount_count[1] += 1
#         result = fabs(macrophages_amount_count[0] / macrophages_amount_count[1] - monocytes_amount_count[0] / monocytes_amount_count[1])
#         if index == 0:
#             first = result
#         if result > first:
#             results[gen[:-1]] += 1
#         macro = set(choices(gens, k=10))
#         mono = set(gens) - macro
#         for x, y in zip(macro, mono):
#             labels_dict[x] = 'macrophages'
#             labels_dict[y] = 'monocytes'
