#!/bin/bash

# Define the source and target file paths
source_file_path="./pipmag/pipmag.py"
target_file_path="./pipmag/functions_and_classes.txt"

# Use grep to find all function and class definitions in the source file
grep -E '^(def|class) ' $source_file_path > $target_file_path
