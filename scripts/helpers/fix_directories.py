import os
import re
import shutil

from params import results_dir

num_trials = 30
num_patterns = 10

run_01_dir = os.path.join(results_dir, 'run_01')
temp_dir = os.path.join(results_dir, 'temp_01')
subdirs = [os.path.join(run_01_dir, d) for d in os.listdir(run_01_dir) if os.path.isdir(os.path.join(run_01_dir, d))]

subdirs.sort()
for subdir in subdirs:
  dir_name = os.path.basename(subdir)
  match = re.match(r'(\w+)_trial_(\d+)_pattern_(\d+)', dir_name)
  if match:
    group = match[1]
    old_trial = int(match[2])
    old_pattern = int(match[3])

    # print(group, old_trial, old_pattern)

    correct_trial = (10 * old_trial + old_pattern) % num_trials
    correct_pattern = old_trial // 3

    # print(old_trial, old_pattern, '-', correct_trial, correct_pattern)

    new_name = f"{group}_trial_{correct_trial}_pattern_{correct_pattern}"

    temp_path = os.path.join(os.getcwd(), temp_dir, new_name)
    original_path = os.path.join(os.getcwd(), subdir)

    # print(temp_path, original_path)

    if not os.path.exists(temp_path):
      shutil.move(original_path, temp_path)
      print(f"Moved '{original_path}' to '{temp_path}'")
    else:
      print(f"Skipping '{original_path}' because '{temp_path}' already exists")
