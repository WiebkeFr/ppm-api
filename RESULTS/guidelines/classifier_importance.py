import numpy as np
from matplotlib import pyplot as plt

features = ['#total_events', '#events', '#traces', 'min_trace', 'max_trace',
       'avg_trace', 'l_detail', 'lz_compl', 'unique_t', 'struc', 'avg_aff',
       'dev_rand', '#ties', 'var_ent', 'nvar_ent', 'seq_ent',
       'nseq_ent']

means = {
    'Fold=4': (0.3206, 0.0579, 0.077, 0.0, 0.0, 0.1717, 0.066, 0.1262, 0.0199, 0.0392, 0.0592, 0.0, 0.0, 0.0, 0.0444, 0.018, 0.0),
    'Fold=5': (0.3597, 0.0418, 0.0285, 0.0, 0.0381, 0.2642, 0.0773, 0.0952, 0.0, 0.0219, 0.0406, 0.0, 0.0, 0.0077, 0.0, 0.0251, 0.0)
}

std = {
    'Fold=4': (0.1642, 0.0722, 0.154, 0.0, 0.0, 0.0483, 0.0763, 0.1457, 0.0398, 0.0783, 0.1183, 0.0, 0.0, 0.0, 0.0531, 0.0361, 0.0),
    'Fold=5': (0.2456, 0.0617, 0.0637, 0.0, 0.057, 0.0571, 0.0821, 0.1309, 0.0, 0.0489, 0.0569, 0.0, 0.0, 0.0172, 0.0, 0.0562, 0.0),
}

means2 = {
    'Fold=4': (0.03609375, 0.012951334379905827, 0.0, 0.050164835164835164, 0.03777472527472528, 0.0, 0.0, 0.0, 0.037774725274725286, 0.06770311149524637, 0.6036913645644082, 0.037774725274725286, 0.030219780219780223, 0.0, 0.0, 0.0, 0.08585164835164837),
    'Fold=5': (0.0, 0.0, 0.06341677646025473, 0.0, 0.0, 0.026785714285714295, 0.02160493827160493, 0.0924096032791685, 0.04822530864197531, 0.07240202789504038, 0.4855405313285748, 0.07111435742388124, 0.0, 0.025925925925925918, 0.0, 0.0, 0.09257481648785995)
}

std2 = {
    'Fold=4': (0.07218749999999999, 0.025902668759811655, 0.0, 0.05846102205836537, 0.07554945054945056, 0.0, 0.0, 0.0, 0.07554945054945057, 0.059532598813394406, 0.22642324314215842, 0.07554945054945057, 0.06043956043956045, 0.0, 0.0, 0.0, 0.1717032967032967),
    'Fold=5': (0.0, 0.0, 0.14180422307903806, 0.0, 0.0, 0.059894677968744384, 0.048310110624995434, 0.12653747409385308, 0.10783506835936485, 0.06923301865351482, 0.15124469109418237, 0.10915887435732541, 0.0, 0.05797213274999453, 0.0, 0.0, 0.10789988080862133),
}

mean = means2
std = std2

x = np.arange(len(features))  # the label locations
width = 0.35  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained', figsize=(10, 3))

for attribute, measurement in means.items():
    offset = width * multiplier
    print(x + offset)
    rects = ax.bar(x + offset, measurement, width, label=attribute, yerr=std[attribute])
    # ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Mean decrease in impurity')
ax.set_xlabel('Features')
print(x + width/2)
ax.set_xticks(x + width / 2, features, rotation=40, ha='right')
ax.legend(loc='upper right', ncols=3)
ax.set_ylim(bottom=0)
ax.grid(axis="y")
ax.set_axisbelow(True)

plt.savefig("classifier_feature_comparison_enc.png", dpi=300)