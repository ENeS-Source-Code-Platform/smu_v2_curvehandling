import csv

import numpy as np


def read_curve_data(filename):
    with open(filename, 'r', encoding='utf-8-sig') as data_file:
        csv_reader = csv.reader(data_file)
        rows = [row for row in csv_reader]
        data = np.array(rows).astype(float).T
        data_file.close()
    return data[0], data[1]


def is_increasing_sequence(x_list):
    for i in range(len(x_list) - 1):
        if x_list[i+1] - x_list[i] >= 0:
            continue
        else:
            return False
    return True


def sort_sequences(x, y):
    temp = np.array([x, y]).T
    tuples_to_be_sorted = []
    for sub_list in temp:
        tuples_to_be_sorted.append((sub_list[0], sub_list[1]))
    tuples_to_be_sorted.sort(key=lambda x: x[0])
    sorted_list = np.array(tuples_to_be_sorted).T
    return sorted_list[0], sorted_list[1]


def handle_negative_value(y_list):
    for i in range(len(y_list)):
        if y_list[i] < 0:
            y_list[i] = 0

    return y_list


def curve_interpolation(x, y, freq):
    start = x[0]
    end = x[-1]

    resampling_points_x = np.linspace(start, end, freq)
    resampling_points_y = np.interp(resampling_points_x, x, y)

    normalized_y = resampling_points_y / np.max(resampling_points_y)

    return normalized_y

