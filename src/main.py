import csv
import os

import numpy as np
import matplotlib.pyplot as plt

from util import read_curve_data, is_increasing_sequence, handle_negative_value, curve_interpolation, sort_sequences

from dirty_samples import get_dirty_samples
from non_standard_samples import get_non_standard_samples
from unclear_samples import get_unclear_samples

with open('./source/labels.csv', 'r', encoding='utf-8-sig') as f:
    csv_reader = csv.reader(f)
    rows = [row for row in csv_reader]
    samples = [[row[col] for row in rows] for col in range(len(rows[0]))]
    f.close()

number_list = samples[0]
label_list = samples[3]
qmax_list = samples[5]
vt_list = samples[8]

vt_list = np.array(vt_list).astype(float)

unclear_samples = get_unclear_samples()
dirty_samples = get_dirty_samples()
non_standard_samples = get_non_standard_samples()

curve_consequences = []

with open('./ERROR', 'w') as error_file:
    for i in range(len(number_list)):
        _number = number_list[i]
        print('Handling ' + _number)
        if (dirty_samples.count(_number) > 0) | (non_standard_samples.count(_number) > 0) | (unclear_samples.count(_number) > 0):
            continue
        filename = str(_number) + '.csv'
        full_path = './source/curve_data/' + filename
        if os.path.exists(full_path) & os.path.isfile(full_path):
            raw_data_x, raw_data_y = read_curve_data(full_path)
            raw_data_x = np.insert(raw_data_x, 0, 0)
            raw_data_y = np.insert(raw_data_y, 0, 0)

            # sort the x series.
            raw_data_x, raw_data_y = sort_sequences(raw_data_x, raw_data_y)

            if not is_increasing_sequence(raw_data_x):
                error_file.write(_number + ' is not a monotonically increasing sequence.\n')
                continue

            if abs(raw_data_x[-1] - vt_list[i]) > 1:
                error_file.write(_number + ' time is not correct. Receive ' + str(raw_data_x[-1]) + '. Expect ' + str(vt_list[i]) + '\n')
                continue

            if abs(float(np.max(raw_data_y)) - float(qmax_list[i])) > 2:
                error_file.write(_number + ' qmax is not correct. Receive ' + str(np.max(raw_data_y)) + '. Expect ' + str(qmax_list[i]) + '\n')
                continue

            raw_data_y = handle_negative_value(raw_data_y)

            # repair start and end.
            raw_data_x[-1] = vt_list[i]

            raw_data_y[-1] = 0

            handled_y = curve_interpolation(raw_data_x, raw_data_y, 200)
            curve_handled_result = [_number, label_list[i]]
            curve_handled_result.extend(handled_y)
            curve_consequences.append(curve_handled_result)

            plot_x = range(200)
            plt.plot(plot_x, handled_y, color='black', linewidth=1)
            plt.savefig('./output/figs/' + _number + '.jpg')

        else:
            error_file.write(_number + ' not exists.\n')

    error_file.close()

with open('./curve_handled.csv', 'w') as output_file:
    csv_writer = csv.writer(output_file)
    for curve in curve_consequences:
        csv_writer.writerow(curve)
    output_file.close()
print('Finish!')
