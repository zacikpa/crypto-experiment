#!/usr/bin/python3

import os
import subprocess

CONFIG_DIR = "config"
ANALYSIS_SCRIPT = "../diffkemp-analysis/analyze.py"
DIFFKEMP_BINARY = "../diffkemp/bin/diffkemp"
RESULTS_DIFF_SCRIPT = "./diffkemp-analysis/results-diff.py"
RESULTS_DIR = "results"
RESULTS_FILENAME = "results.yml"
DIFF_FILENAME = "diff.yml"
ALL_PATTERNS_RESULTS_DIR = os.path.join(RESULTS_DIR, "all-patterns")
ALL_PATTERNS_RESULTS_FILE = os.path.join(ALL_PATTERNS_RESULTS_DIR, "results.yml")
DISABLED_PATTERNS = ["group-vars", "reordered-bin-ops"]

BUILTIN_PATTERNS = [
    "struct-alignment",
    "function-splits",
    "numerical-macros",
    "relocations",
    "inverse-conditions",
]

for config_filename in os.listdir(CONFIG_DIR):
    config_filepath = os.path.join(CONFIG_DIR, config_filename)
    analysis_cmd = [
        ANALYSIS_SCRIPT,
        config_filepath,
        "--diffkemp",
        DIFFKEMP_BINARY,
        "--disable-patterns",
        ",".join(DISABLED_PATTERNS),
        "--output",
        ALL_PATTERNS_RESULTS_DIR,
    ]
    subprocess.run(analysis_cmd)

    for pattern in BUILTIN_PATTERNS:
        results_dir = os.path.join(RESULTS_DIR, pattern)
        results_file = os.path.join(results_dir, RESULTS_FILENAME)
        disabled_patterns = DISABLED_PATTERNS + [pattern]
        analysis_cmd = [
            ANALYSIS_SCRIPT,
            config_filepath,
            "--diffkemp",
            DIFFKEMP_BINARY,
            "--disable-patterns",
            ",".join(disabled_patterns),
            "--output",
            results_dir,
        ]
        subprocess.run(analysis_cmd)
        diff_file = os.path.join(results_dir, "diff.yml")
        diff_cmd = [
            RESULTS_DIFF_SCRIPT,
            ALL_PATTERNS_RESULTS_FILE,
            results_file,
            "--output",
            diff_file,
        ]
        subprocess.run(diff_cmd)
