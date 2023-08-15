import json
from time import time
import os
import pickle


from evaluate_dataset.complexity import measure_lempel_ziv, measure_deviation_from_random, generate_pm4py_log, \
    generate_log, measure_affinity, measure_trace_length, aux_event_classes, measure_support, measure_magnitude, \
    measure_distinct_traces, measure_structure, measure_level_of_detail, measure_variety, build_graph, \
    measure_pentland_task, graph_complexity, log_complexity

path = os.path.join(os.curdir, "evaluate_dataset", "decision_tree_technique.sav")
clf = pickle.load(open(path, 'rb'))
scaler = pickle.load(open("evaluate_dataset/min_max_scaler.sav", 'rb'))

def event_log_assessment(id):
    path = os.path.join(os.curdir, "data", "logs", id)
    print(path)

    pm4py_log = generate_pm4py_log(path)
    log = generate_log(pm4py_log)
    pa = build_graph(log)

    start_time = time()

    measures = {}

    # SIZE: Returns the number of events in the event log
    measures['#total_events'] = measure_magnitude(log)

    # SIZE: Returns the number of event classes in the event log
    measures['#events'] = measure_variety(pm4py_log)

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
    measures['#ties'] = measure_pentland_task(pa)

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

    # GRAPH: Trace Entropy
    var_ent = graph_complexity(pa)
    measures['var_ent'] = var_ent[0]
    measures['nvar_ent'] = var_ent[1]

    seq_ent = log_complexity(pa)
    measures['seq_ent'] = seq_ent[0]
    measures['nseq_ent'] = seq_ent[1]

    end_time = time()
    measures['time'] = end_time - start_time

    return measures


def set_config_suggestion(id):
    filename =  f"{id}.json"
    eval_path = os.path.join(os.curdir, "data", "evaluations", filename)
    features = ['#total_events', '#events', '#traces', 'max_trace', 'avg_trace', 'l_detail', 'lz_compl', 'unique_t', 'struc', 'avg_aff', 'nvar_ent', 'seq_ent']

    with open(eval_path) as f:
        complexity = json.load(f)

        sample = [complexity[feature] for feature in features]
        scaled_row = scaler.transform([sample])
        pred_result = clf.predict(scaled_row)[0]
        pred_prob_result = clf.predict_proba(scaled_row)[0]

        print(pred_result)
        print(pred_prob_result)
        return {'type': pred_result }
