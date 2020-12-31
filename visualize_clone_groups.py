import matplotlib.pyplot as plt
import matplotlib.ticker
import analysis.clone_group_analysis.clone_group_analysis as clone_analysis
import data_preparation.data_grouping as data_load
import collections

def xy_axes_clone_group_size_to_number_of_groups(sstubs_to_plot):
    size_to_clone_groups = clone_analysis.classify_clone_groups_by_size(sstubs_to_plot)

    size_to_clone_groups = collections.OrderedDict(sorted(size_to_clone_groups.items()))

    x_arr = []
    y_arr = []
    for k, v in size_to_clone_groups.items():
        x_arr.append(k)
        y_arr.append(len(v))
    return (x_arr, y_arr)

all_sstubs = data_load.exclude_buckets_with_single_sstubs(data_load.load_raw_grouped_sstubs())
sstubs_with_digits_only = data_load.exclude_sstubs_with_letters(all_sstubs)
valid_sstubs = data_load.exclude_sstubs_with_digits_only(all_sstubs)

total = 0
for proj, clone_groups_for_proj in valid_sstubs.items():
    total += len(clone_groups_for_proj)
print(f"Total valid clone groups: {total}")

x_arr_digits, y_arr_digits = xy_axes_clone_group_size_to_number_of_groups(sstubs_with_digits_only)

x_arr_valid, y_arr_valid = xy_axes_clone_group_size_to_number_of_groups(valid_sstubs)

plt.figure(figsize=(10, 5))
ax1 = plt.subplot(1, 2, 1)
ax1.set_yscale("log", base = 2)
ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.xlabel("Clone Group Size")
plt.ylabel("Number of Clone Groups with digits only for given size")
plt.bar(x_arr_digits, y_arr_digits)

ax2 = plt.subplot(1, 2, 2)
ax2.set_yscale("log", base = 2)
ax2.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.xlabel("Clone Group Size")
plt.ylabel("Number of Valid Clone Groups for given size")
plt.bar(x_arr_valid, y_arr_valid)

plt.show()