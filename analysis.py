from datetime import date
from math import ceil
from os import listdir
from os.path import isfile, join

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def percent(nb_case, total) -> float:
    '''Return the percentage'''
    return ceil(nb_case / total * 10000)/100


def prepare_dataset(directory: str, output_file: str):
    """Merging of all annotations files in one, plus one-hot encoding and splitting of columns with multiple values allowed.
    To be run before analysis.

    directory: the path to the directory containing the annotations files.

    output_file: file containing the results of the aforementioned processing.
    """
    print("data preparation...")
    header = ["expression", "plurality", "Yago4", "manifestation_named",
              "manifestation_undetermined",
              "manifestation_determined",
              "manifestation_numbered",
              "manifestation_anaphora",
              "manifestation_qualified_anaphora",
              "manifestation_mass_noun",
              "manifestation_contains_named",
              "modifiers_adjective",
              "modifiers_preposition",
              "modifiers_noun",
              "vagueness_degree",
              "vagueness_portions",
              "vagueness_subjective",
              "vagueness_NOT_VAGUE"
              ]

    lines = ["\t".join(header)]

    for file_name in [file_name for file_name in listdir(directory) if isfile(join(directory, file_name))]:
        full_path = join(directory, file_name)
        with open(full_path) as f:
            for line in f.readlines()[1:]:
                striped_line = line.strip().lower()
                # skip empty lines
                if striped_line == "" or striped_line.startswith("xxx"):
                    continue

                # skip comments
                if "xxx" in striped_line:
                    index = striped_line.index("xxx")
                    striped_line = striped_line[:index].strip()
                cols = striped_line.split("\t")
                line_dict = {}

                line_dict["expression"] = cols[0]
                line_dict["plurality"] = cols[1]
                line_dict["Yago4"] = cols[2]
                col = cols[3]
                line_dict["manifestation_contains_named"] = 1 if "contains_named" in col else 0
                line_dict["manifestation_named"] = 1 if "named" in col and "contains_named" not in col else 0
                line_dict["manifestation_undetermined"] = 1 if "undetermined" in col else 0
                line_dict["manifestation_determined"] = 1 if "determined" in col and "undetermined" not in col else 0
                line_dict["manifestation_numbered"] = 1 if "numbered" in col else 0
                line_dict["manifestation_anaphora"] = 1 if "anaphora" in col and "qualified_anaphora" not in col else 0
                line_dict["manifestation_qualified_anaphora"] = 1 if "qualified_anaphora" in col else 0
                line_dict["manifestation_mass_noun"] = 1 if "mass_noun" in col else 0
                col = cols[4]
                line_dict["modifiers_adjective"] = 1 if "adjective" in col else 0
                line_dict["modifiers_preposition"] = 1 if "preposition" in col else 0
                line_dict["modifiers_noun"] = 1 if "noun" in col else 0
                col = cols[5]
                line_dict["vagueness_degree"] = 1 if "degree" in col else 0
                line_dict["vagueness_portions"] = 1 if "portions" in col else 0
                line_dict["vagueness_subjective"] = 1 if "subjective" in col else 0
                line_dict["vagueness_NOT_VAGUE"] = 1 if "not_vague" in col else 0

                if line_dict["vagueness_NOT_VAGUE"] == 1 and (line_dict["vagueness_degree"] + line_dict["vagueness_portions"] + line_dict["vagueness_subjective"]) > 0:
                    print("err")

                line_arr = [
                    line_dict["expression"],
                    line_dict["plurality"],
                    line_dict["Yago4"],
                    line_dict["manifestation_named"],
                    line_dict["manifestation_undetermined"],
                    line_dict["manifestation_determined"],
                    line_dict["manifestation_numbered"],
                    line_dict["manifestation_anaphora"],
                    line_dict["manifestation_qualified_anaphora"],
                    line_dict["manifestation_mass_noun"],
                    line_dict["manifestation_contains_named"],
                    line_dict["modifiers_adjective"],
                    line_dict["modifiers_preposition"],
                    line_dict["modifiers_noun"],
                    line_dict["vagueness_degree"],
                    line_dict["vagueness_portions"],
                    line_dict["vagueness_subjective"],
                    line_dict["vagueness_NOT_VAGUE"]
                ]

                # check if errors appears when editing the annotations files
                if len(line_arr) != len(header):
                    error_message = f"length error in {full_path}, line: {line}\nLength is {len(line_arr)} and should have been {len(header)}!"
                    print(error_message)
                    raise Exception(error_message)
                line = ""
                for el in line_arr:
                    line += str(el).strip() + "\t"
                lines.append(line.strip())

    print("saving results...")
    with open(output_file, 'w') as f:
        for line in lines:
            f.write(line + "\n")
    print(f"data from {directory} have been processed in {output_file}")


def comput_stats(dataset_path):
    """Compute generic stats about the dataset, then more fine grained stats like percentage by vagueness types according to the dimensions."""
    selected_header = [  # "plurality", "Yago4",
        "manifestation_named",
        "manifestation_undetermined",
        "manifestation_determined",
        "manifestation_numbered",
        "manifestation_anaphora",
        "manifestation_qualified_anaphora",
        "manifestation_mass_noun",
        "manifestation_contains_named",
        "modifiers_adjective",
        "modifiers_preposition",
        "modifiers_noun",
    ]
    vagueness_types = [
        "vagueness_degree",
        "vagueness_portions",
        "vagueness_subjective",
        # "vagueness_NOT_VAGUE"
    ]

    data = pd.read_csv(dataset_path, sep="\t", header=0)

    tot = len(data)
    print(f"# of NPs: {tot}")
    cur = len(data.loc[(data["vagueness_degree"] == 1) | (
        data["vagueness_portions"] == 1) | (data["vagueness_subjective"] == 1)])
    print(f"# of vague NPs: {cur} ({percent(cur, tot)}%)")
    multiple_vagueness = len(data.loc[((data["vagueness_degree"] == 1) & ((data["vagueness_portions"] == 1) | (
        data["vagueness_subjective"] == 1)) | ((data["vagueness_portions"] == 1) & (data["vagueness_subjective"] == 1)))])
    print(
        f"# of multiple vague NPs: {multiple_vagueness} (with all NP: {percent(multiple_vagueness, tot)}%, among vague NPs: {percent(multiple_vagueness, cur)}%)")
    # exit(0)
    cur = len(data.loc[data["vagueness_degree"] == 1])
    print(f"# of vagueness_degree NPs: {cur} ({percent(cur, tot)}%)")
    cur = len(data.loc[data["vagueness_portions"] == 1])
    print(f"# of vagueness_portions NPs: {cur} ({percent(cur, tot)}%)")
    cur = len(data.loc[data["vagueness_subjective"] == 1])
    print(f"# of vagueness_subjective NPs: {cur} ({percent(cur, tot)}%)")

    cur = len(data.loc[data["plurality"] == "instance"])
    print(f"# of instance NPs: {cur} ({percent(cur, tot)}%)")
    cur = len(data.loc[data["plurality"] == "class"])
    print(f"# of class NPs: {cur} ({percent(cur, tot)}%)")

    today = date.today().strftime("%Y%m%d")

    # modifiers and manifestations
    with open(f"{today} percentage of all XXX vague noun phrases having a YYY modifier or manifestation.tsv", 'w', encoding="utf-8") as output:
        for v_type in vagueness_types:
            vague_df = data.loc[data[v_type] == 1]
            total = len(vague_df)
            for mod_type in selected_header:
                mod_vague_df = vague_df.loc[vague_df[mod_type] == 1]
                curr = len(mod_vague_df)
                output.write(
                    f"total # of {v_type}:\t{total}\t# of {mod_type}:\t{curr}\t{percent(curr, total)}%\n")

    with open(f"{today} percentage of all noun phrases with XXX modifier or manifestation being YYY vague.tsv", 'w', encoding="utf-8") as output:
        for mod_type in selected_header:
            vague_df = data.loc[data[mod_type] == 1]
            total = len(vague_df)
            nb_vague = len(vague_df.loc[(vague_df["vagueness_degree"] == 1) | (
                vague_df["vagueness_portions"] == 1) | (vague_df["vagueness_subjective"] == 1)])
            print(
                f"total # of {mod_type}:\t{total}\t# of vague:\t{nb_vague}\t{percent(nb_vague, total)}%\n")
            for v_type in vagueness_types:
                mod_vague_df = vague_df.loc[vague_df[v_type] == 1]
                curr = len(mod_vague_df)
                output.write(
                    f"total # of {mod_type}:\t{total}\t# of {v_type}:\t{curr}\t{percent(curr, total)}%\n")

    # yago classes
    with open(f"{today} percentage of all XXX vague noun phrases having a YYY class.tsv", 'w', encoding="utf-8") as output:
        for v_type in vagueness_types:
            vague_df = data.loc[data[v_type] == 1]
            total = len(vague_df)
            for mod_type in ['creativework', 'biochementity', 'action', 'organization', 'person', 'place', 'taxon', 'intangible', 'medicalentity', 'event', 'product']:
                mod_vague_df = vague_df.loc[vague_df["Yago4"] == mod_type]
                curr = len(mod_vague_df)
                output.write(
                    f"total # of {v_type}:\t{total}\t# of {mod_type}:\t{curr}\t{percent(curr, total)}%\n")
    with open(f"{today} percentage of all noun phrases with XXX class being YYY vague.tsv", 'w', encoding="utf-8") as output:
        for mod_type in ['creativework', 'biochementity', 'action', 'organization', 'person', 'place', 'taxon', 'intangible', 'medicalentity', 'event', 'product']:
            vague_df = data.loc[data["Yago4"] == mod_type]
            total = len(vague_df)
            for v_type in vagueness_types:
                mod_vague_df = vague_df.loc[vague_df[v_type] == 1]
                curr = len(mod_vague_df)
                output.write(
                    f"total # of {mod_type}:\t{total}\t# of {v_type}:\t{curr}\t{percent(curr, total)}%\n")
    with open(f"{today} percentage of all noun phrases with XXX class.tsv", 'w', encoding="utf-8") as output:
        total = len(data)
        lines = list()
        for mod_type in ['creativework', 'biochementity', 'action', 'organization', 'person', 'place', 'taxon', 'intangible', 'medicalentity', 'event', 'product']:
            vague_df = data.loc[data["Yago4"] == mod_type]
            curr = len(vague_df)
            nb_vague = len(vague_df.loc[(vague_df["vagueness_degree"] == 1) | (
                vague_df["vagueness_portions"] == 1) | (vague_df["vagueness_subjective"] == 1)])
            nb_scalar = len(vague_df.loc[vague_df["vagueness_degree"] == 1])
            nb_quant = len(vague_df.loc[vague_df["vagueness_portions"] == 1])
            nb_subj = len(vague_df.loc[vague_df["vagueness_subjective"] == 1])
            # output.write(f"total # of NPs:\t{total}\t# of {mod_type}:\t{curr}\t{percent(curr, total)}%\tvague:\t{nb_vague}\t{percent(nb_vague, curr)}\tscalar:\t{nb_scalar}\t{percent(nb_scalar, curr)}\tquantitative:\t{nb_quant}\t{percent(nb_quant, curr)}\tsubjective:\t{nb_subj}\t{percent(nb_subj, curr)}\n")
            line = f"{mod_type} & {curr} & {nb_vague} & {percent(nb_vague, curr)}\% & {nb_scalar} & {percent(nb_scalar, curr)}\% &{nb_quant} & {percent(nb_quant, curr)}\% & {nb_subj} & {percent(nb_subj, curr)}\% \\\\\n"
            lines.append((curr, line))
            # output.write(line) # for human reader
        lines = sorted(lines, key=lambda tup: tup[0], reverse=True)
        for l in lines:
            output.write(l[1])  # for latex

    # plurality
    with open(f"{today} percentage of all XXX vague noun phrases having a YYY plurality.tsv", 'w', encoding="utf-8") as output:
        for v_type in vagueness_types:
            vague_df = data.loc[data[v_type] == 1]
            total = len(vague_df)
            for mod_type in ['instance', 'class']:
                mod_vague_df = vague_df.loc[vague_df["plurality"] == mod_type]
                curr = len(mod_vague_df)
                output.write(
                    f"total # of {v_type}:\t{total}\t# of {mod_type}:\t{curr}\t{percent(curr, total)}%\n")
    with open(f"{today} percentage of all noun phrases with XXX plurality being YYY vague.tsv", 'w', encoding="utf-8") as output:
        for mod_type in ['instance', 'class']:
            vague_df = data.loc[data["plurality"] == mod_type]
            total = len(vague_df)
            for v_type in vagueness_types:
                mod_vague_df = vague_df.loc[vague_df[v_type] == 1]
                curr = len(mod_vague_df)
                output.write(
                    f"total # of {mod_type}:\t{total}\t# of {v_type}:\t{curr}\t{percent(curr, total)}%\n")


def compute_correlation(dataset_path):
    """Compute all correlations, then meaningful correlations."""
    frame = pd.read_csv(dataset_path, sep='\t', header=0)
    frame.drop(['expression',
                # 'undetermined',
                # 'determined',
                # 'vagueness_degree',
                # 'vagueness_portions', 'vagueness_subjective', 'vagueness_NOT_VAGUE',
                # 'manifestation_named',
                # 'mass_noun',
                # 'adjective',
                # 'degree',
                # 'portions',
                # 'subjective',
                # 'vague'
                ], inplace=True, axis=1)

    frame_onehot = frame.copy()
    cols = ['plurality', 'Yago4']
    frame_onehot = pd.get_dummies(
        frame_onehot, columns=cols)
    corr_matrix = frame_onehot.corr()

    # correlation matrix
    c = corr_matrix.abs()
    s = c.unstack()
    so = s.sort_values(ascending=False)  # kind="quicksort")

    today = date.today().strftime("%Y%m%d")

    with open(f"{today}_all_correlation.csv", "w") as f:
        so.to_csv(f)
    with open(f"{today}_all_correlation.csv") as f:
        lines = ["d1,d2,value\n"]
        couples = set()
        for line in f.readlines()[1:]:
            if line.strip() == "":
                continue
            if "vagueness" not in line:
                continue
            cols = line.split(",")
            if "1.0" in cols[-1]:
                continue
            if cols[0][0:3] == cols[1][0:3]:
                continue
            if (cols[0] + cols[1]) in couples or (cols[1] + cols[0]) in couples:
                continue
            else:
                couples.add(cols[0] + cols[1])
            # tab = ["portions", "degree", "vague", "subjective"]
            # if cols[0] not in tab and cols[1] in tab:
            #     lines.append(line)
            lines.append(line)
        with open(f"{today}_interesting_correlations.csv", 'w') as out:
            out.writelines(lines)

    plt.pcolor(corr_matrix)
    plt.yticks(np.arange(0.5, len(corr_matrix.index), 1), corr_matrix.index)
    plt.xticks(np.arange(0.5, len(corr_matrix.columns), 1),
               corr_matrix.columns)
    plt.setp(plt.gca().get_xticklabels(),
             rotation=30, horizontalalignment='right')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    dataset_path = "dataset_{0}.tsv".format(date.today().strftime("%Y%m%d"))
    directory = "data/annotations"

    # first we need to prepare the data
    prepare_dataset(directory, dataset_path)
    # then we compute statistics
    comput_stats(dataset_path)
    # and finally, we compute correlations
    compute_correlation(dataset_path)

    print("end")
