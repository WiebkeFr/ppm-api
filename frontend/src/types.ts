export interface Measurement {
  "#events": number;
  "#activity": number;
  "#traces": number;
  min_trace: number;
  max_trace: number;
  avg_trace: number;
  time: number;
  lz_compl: number;
  l_detail: number;
  unique_t: string;
  struc: number;
  t_div: number;
  var_ent: number;
  norm_var_ent: number;
  seq_ent: number;
  norm_seq_ent: number;
}

export const Measurement_Names: {
  [key: string]: string;
} = {
  "#events": "Total number of events",
  "#activity": "Total number of event classes",
  "#traces": "Total number of traces",
  min_trace: "Minimum trace length",
  max_trace: "Maximum trace length",
  avg_trace: "Average trace length",
  l_detail: "Number of Acyclic Paths in Transition Matrix",
  time: "Duration",
  lz_compl: "Lempel–Ziv Complexity",
  avg_aff: "Average Affinity",
  dev_rand: "Deviation from random",
  unique_t: "Percentage of unique traces",
  struc: "Average Distinct Events per traces structure",
  t_div: "Trace Diversity",
  var_ent: "Variant Entropy",
  norm_var_ent: "Normalized Variant Entropy",
  seq_ent: "Sequence Entropy",
  norm_seq_ent: "Normalized sequence Entropy"
};

export interface AdditionalInfoCsv {
  isWithHeader: boolean;
  delimiter: string;
  caseIdColumn: number;
  activityColumn: number;
  timestampColumn: number;
}

export const TrainingInfoOptions = [
  {
    label: "Model-Typ",
    key: "type",
    options: [
      {
        key: "LSTM",
        label: "Long short term memory",
      },
      {
        key: "CNN",
        label: "Convolutional neural network",
      },
      {
        label: "Decision Tree",
        key: "DT",
      },
    ],
  },
  {
    label: "Sequence-Encoding",
    key: "sequ_enc",
    options: [
      {
        key: "PREPAD",
        label: "Prefix padded",
      },
      {
        key: "CONT",
        label: "Continous (window-size: 4)",
      },
    ],
  },
  {
    label: "Event-Encoding",
    key: "event_enc",
    options: [
      {
        key: "ONEHOT",
        label: "One-hot-encoding",
      },
      {
        key: "EMBEDDED",
        label: "Embedding",
      },
      {
        key: "FREQBASED",
        label: "Frequency-based",
      },
    ],
  },
];

export interface TrainingInfoSelection {
  type: string;
  sequ_enc: string;
  event_enc: string;
}
