import sys
import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


pdcNegative, pdcPositive, pdcUncertain, pdcNotCalculated = 0, 1, 2, 3
call_mapping = {'pdcNegative': pdcNegative, 'pdcNotCalculated': pdcNotCalculated, 'pdcPositive': pdcPositive, 'pdcUncertain': pdcUncertain}


filename, directory1, directory2 = sys.argv[1:]
t = pd.read_csv(filename, sep='\t')

exps = [expname for expname in t["Experiment Name"]]
# print("\n".join(sorted(exps)))


def exists(expname, directory1, directory2):
    path1 = os.path.join(directory1, expname + ".txt")
    path2 = os.path.join(directory2, expname + ".txt")
    if os.path.exists(path1):
        return path1
    elif os.path.exists(path2):
        return path2
    else:
        return None


def read(filename):
    t = pd.read_csv(filename, sep='\t')

    cols = t.columns.values.tolist()
    pre_df = {}
    try:
        p1 = re.compile('^[A-Z][0-9]*: Sample [0-9-]*$')
        p2 = re.compile('^[A-Z][0-9]*: [0-9-]*$')
        for col in cols:
            assert col == "X" or col.startswith("X.") or bool(p1.match(col)) or bool(p2.match(col)), f"{col} name invalid"

        for col in cols:
            if col.startswith("X"):
                assert tuple(t[col]) == tuple(range(1, 46))
        for col in cols:
            if bool(p1.match(col)) or bool(p2.match(col)):
                series = t[col].to_numpy()
                assert series.shape == (45, )
                pre_df[col] = series
    except AssertionError:
        raise
    return pd.DataFrame(pre_df)

expnames = t["Experiment Name"].unique()
exists_errors = 0
format_errors = 0
total_files = 0
datasets = {}
for expname in expnames:
    total_files += 1
    path = exists(expname, directory1, directory2)
    if path is None:
        exists_errors += 1
        continue
    try:
        data = read(path)
        if data is not None:
            datasets[expname] = data
    except AssertionError:
        format_errors += 1

print(f"{exists_errors} missing file errors, {format_errors} malformed file errors out of total {total_files} files")


total = 0
missing_file = 0
missing_column = 0
collect = []
calls = []
for expname, position, sample_name, call in zip(t["Experiment Name"], t["Position"], t["SampleName"], t["Call"]):
    total += 1
    if expname not in datasets:
        missing_file += 1
        continue
    column_name = position + ": " + sample_name
    if column_name not in datasets[expname]:
        missing_column += 1
        continue
    collect.append(datasets[expname][column_name])
    calls.append(call_mapping[call])
    if total % 1000 == 0:
        n = len(t["Experiment Name"])
        print(f"{total} out of {n} items", file=sys.stderr)

collect = np.array(collect)
calls = np.array(calls)
print("collected", collect.shape, calls.shape, collect.dtype, calls.dtype)

print(f"{missing_file} samples had their file missing or malformed, {missing_column} samples had their column missing from their file.")


merged = np.concatenate([calls[:, None], collect], axis=1)

assert merged.dtype == np.float64

np.save("pcr.npy", merged)
