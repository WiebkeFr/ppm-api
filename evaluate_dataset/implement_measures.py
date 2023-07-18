from pm4py.algo.filtering.log.attributes import attributes_filter as log_attributes_filter


# general helpers
def event_names(log):
    events = log_attributes_filter.get_attribute_values(log, "concept:name")
    event_list = [*events]
    return event_list


def total_number_of_events(log):
    return sum(len(case) for case in log)


def total_number_of_event_classes(log):
    return len(event_names(log))


def total_number_of_traces(log):
    return len(log)


def minimum_trace_length(log):
    mint = log.groupby(["case:concept:name"])["case:concept:name"].count().min()
    return mint.item()
    # return min([len(case) for case in log])


def maximum_trace_length(log):
    maxl = log.groupby(["case:concept:name"])["case:concept:name"].count().max()
    return maxl.item()
    # return min([len(case) for case in log])


def average_trace_size(log):
    return log.groupby(["case:concept:name"])["case:concept:name"].count().mean()
    # return len([(event["concept:name"]) for case in log for event in case]) / len(log)
