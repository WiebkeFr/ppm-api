from time import time
import os

from evaluate_dataset.complexity import measure_lempel_ziv, measure_deviation_from_random, generate_pm4py_log, \
    generate_log, measure_affinity, measure_trace_length, aux_event_classes, measure_support, measure_magnitude, \
    measure_distinct_traces, measure_structure, measure_level_of_detail, measure_variety, build_graph, \
    measure_pentland_task


def event_log_assessment(id):
    path = os.path.join(os.curdir, "data", "logs", id)
    print(path)

    pm4py_log = generate_pm4py_log(path)

    print(pm4py_log[:3])

    log = generate_log(pm4py_log)
    print(log[:3])
    pa = build_graph(log)

    start_time = time()

    measures = {}

    # SIZE: Returns the number of events in the event log
    measures['#events'] = measure_magnitude(log)

    # SIZE: Returns the number of event classes in the event log
    measures['#activity'] = measure_variety(pm4py_log)

    # SIZE: Returns the number of traces in the event log
    measures['#traces'] = measure_support(pm4py_log)

    # SIZE: Returns length of shortest trace
    # SIZE: Returns length of longest trace
    # SIZE: Average trace size (i.e. number of event classes per case (trace))
    trace_lengths = measure_trace_length(pm4py_log)
    measures['min_trace'] = trace_lengths["min"]
    measures['max_trace'] = trace_lengths["max"]
    measures['avg_trace'] = trace_lengths["avg"]

    # VARIATION: Number of Acyclic Paths in Transition Matrix
    measures['l_detail'] = measure_level_of_detail(pm4py_log)

    # VARIATION: Number of Ties in Transition Matrix


    # VARIATION: Lempel–Ziv Complexity
    measures['lz_compl'] = measure_lempel_ziv(log)

    # VARIATION: Number and Percentage of unique traces
    measures['unique_t'] = measure_distinct_traces(pm4py_log)

    # VARIATION: Average Distinct Events per traces structure
    measures['struc'] = measure_structure(pm4py_log)

    # DISTANCE: Average Affinity
    measures['avg_aff'] = measure_affinity(pm4py_log)

    # DISTANCE: Deviation from random:
    measures['dev_rand'] = measure_deviation_from_random(log, pm4py_log)

    # DISTANCE: Trace Diversity
    measures['t_div'] = measure_pentland_task(pa)

    # GRAPH: Trace Entropy

    end_time = time()
    measures['time'] = end_time - start_time

    return measures
