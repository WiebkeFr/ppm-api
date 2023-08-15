export interface Measurement {
  "#total_events": number;
  "#events": number;
  "#traces": number;
  min_trace: number;
  max_trace: number;
  avg_trace: number;
  time: number;
  lz_compl: number;
  l_detail: number;
  unique_t: string;
  struc: number;
  "#ties": number;
  var_ent: number;
  nvar_ent: number;
  seq_ent: number;
  nseq_ent: number;
}

export const Measurement_Names: {
  [key: string]: string;
} = {
  "#total_events": "Total number of events",
  "#events": "Total number of event classes",
  "#traces": "Total number of traces",
  min_trace: "Minimum trace length",
  max_trace: "Maximum trace length",
  avg_trace: "Average trace length",
  l_detail: "Number of Acyclic Paths in Transition Matrix",
  "#ties": "Number of Ties in Transition Matrix",
  time: "Duration",
  lz_compl: "Lempel–Ziv Complexity",
  avg_aff: "Average Affinity",
  dev_rand: "Deviation from Random",
  unique_t: "Percentage of unique Traces",
  struc: "Average Distinct Events per Traces Structure",
  var_ent: "Variant Entropy",
  nvar_ent: "Normalized Variant Entropy",
  seq_ent: "Sequence Entropy",
  nseq_ent: "Normalized sequence Entropy"
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
