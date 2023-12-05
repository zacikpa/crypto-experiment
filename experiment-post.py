#!/usr/bin/python3

import os
import subprocess

CONFIG_DIR = "config"
ANALYSIS_SCRIPT = "../diffkemp-analysis/analyze.py"
DIFFKEMP_BINARY = "../diffkemp/bin/diffkemp"
RESULTS_DIFF_SCRIPT = "../diffkemp-analysis/diff-results.py"
RESULTS_DIR = os.path.join("results", "post")
RESULTS_FILENAME = "results.yml"
DIFF_FILENAME = "diff.yml"
ALL_PATTERNS_RESULTS_DIR = "all-patterns"

LIBRARIES = ["mbedtls-2", "mbedtls-3", "nettle-3", "sodium-1", "wolfssl-4", "wolfssl-5"]

NEW_PATTERNS = [
    "group-vars",
    "reordered-bin-ops",
]

for library in LIBRARIES:
    config_filepath = os.path.join(CONFIG_DIR, f"{library}.yml")
    all_pattern_results_dir = os.path.join(RESULTS_DIR, ALL_PATTERNS_RESULTS_DIR)
    analysis_cmd = [
        ANALYSIS_SCRIPT,
        config_filepath,
        "--diffkemp",
        DIFFKEMP_BINARY,
        "--output",
        all_pattern_results_dir,
    ]
    subprocess.run(analysis_cmd)

    for pattern in NEW_PATTERNS:
        results_dir = os.path.join(RESULTS_DIR, pattern)
        analysis_cmd = [
            ANALYSIS_SCRIPT,
            config_filepath,
            "--diffkemp",
            DIFFKEMP_BINARY,
            "--disable-patterns",
            pattern,
            "--output",
            results_dir,
        ]
        subprocess.run(analysis_cmd)
        diff_file = os.path.join(results_dir, library, DIFF_FILENAME)
        diff_cmd = [
            RESULTS_DIFF_SCRIPT,
            os.path.join(all_pattern_results_dir, library, RESULTS_FILENAME),
            os.path.join(results_dir, library, RESULTS_FILENAME),
            "--output",
            diff_file,
        ]
        subprocess.run(diff_cmd)
