
time python read.py "PCR call értékei/PCR crossingpoints and calls 2021 01-02.txt" "Fluoreszcencia adatok 2021 01 (baseline subst. és csatorna ellenőrzött)" "Fluoreszcencia adatok 2021 02 (baseline subst. és csatorna ellenőrzött)"

22 missing file errors, 2 malformed file errors out of total 249 files
676 samples had their file missing or malformed, 0 samples had their column missing from their file.
collected (21006, 45) (21006,)

# -> pcr.npy
mv pcr.npy pcr.21006.npy

python analyze.py pcr.21006.npy
