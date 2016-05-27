import sys
import os

cur_file = os.path.abspath(os.path.dirname(__file__))
sys.path.append(cur_file + '/../analyzers')
sys.path.append(cur_file + '/../analyzers/constraints')

import ohlc_difference_factor_constraint
import binary_analyzer
import slope_constraint
import json_loader

loader = json_loader.json_loader()

if(len(sys.argv) < 2):
	print('You must supply a json file with analyzer constraints.')
	print('e.g. \"python3 run.py /home/zane/files/secret_folder/amazing_json_constraints.json\"')
	sys.exit(0)

analyzer = loader.load(sys.argv[1])
results = analyzer.check_constraints()

total = len(results)

constraint_results = [0] * (len(results[0][2]) - 1)

hits = 0.0
passed_checks = 0.0

for result in results:
	hit = True
	# iterate over everything but the last item
	# which is the check
	# print(result[2][:-1])
	for key, constraint in enumerate(result[2][:-1]):
		if(constraint == True):
			constraint_results[key] += 1
		else:
			hit = False
	if(hit == True):
		hits += 1
		if(result[2][-1] == True):
			passed_checks += 1

print(constraint_results)
print('hits: '+str(hits))
print('passed checks: '+str(passed_checks))
print('probability of passing given hit: '+str(passed_checks/hits))