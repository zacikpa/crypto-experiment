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
CUSTOM_PATTERNS_CONFIG_FILENAME = "config.yml"
CUSTOM_PATTERNS_DIR = "custom-patterns"

LIBRARIES = ["mbedtls-2", "mbedtls-3", "nettle-3", "sodium-1", "wolfssl-4", "curl-7"]

NEW_PATTERNS = [
    "group-vars",
    "reordered-bin-ops",
]

for library in LIBRARIES:
    config_filepath = os.path.join(CONFIG_DIR, f"{library}.yml")
    all_pattern_results_dir = os.path.join(RESULTS_DIR, ALL_PATTERNS_RESULTS_DIR)
    custom_pattern_config_path = os.path.join(
        CUSTOM_PATTERNS_DIR, library, CUSTOM_PATTERNS_CONFIG_FILENAME
    )
    analysis_cmd = [
        ANALYSIS_SCRIPT,
        config_filepath,
        "--diffkemp",
        DIFFKEMP_BINARY,
        "--output",
        all_pattern_results_dir,
    ]
    if os.path.isfile(custom_pattern_config_path):
        analysis_cmd += ["--custom-patterns", custom_pattern_config_path]
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
        if os.path.isfile(custom_pattern_config_path):
            analysis_cmd += ["--custom-patterns", custom_pattern_config_path]
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
