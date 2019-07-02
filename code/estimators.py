from rumor_center import *

#Estimator 0 -> s1^s2 / s1*s2 - s1^s2
def est_0(s1, s2):
	s1_num = s1.number_of_nodes()
	s2_num = s2.number_of_nodes()

	ov_num = 0
	for i in s1.nodes():
		for j in s2.nodes():
			if i == j:
				ov_num += 1
				break
	normal_fact = (max(s1_num, s2_num) - 1)
	return (float( normal_fact * ov_num / (s1_num*s2_num - ov_num) ))

#Estimator 1 -> s1^s2 / min(s1,s2)
def est_1(s1, s2):
	s1_num = s1.number_of_nodes()
	s2_num = s2.number_of_nodes()

	ov_num = 0
	for i in s1.nodes():
		for j in s2.nodes():
			if i == j:
				ov_num += 1
				break
	#Already normalised
	return (float( ov_num / min(s1_num, s2_num) ))

#Estimator 2 -> s1^s2 / s1vs2
def est_2(s1, s2):
	s1_num = s1.number_of_nodes()
	s2_num = s2.number_of_nodes()

	ov_num = 0
	for i in s1.nodes():
		for j in s2.nodes():
			if i == j:
				ov_num += 1
				break

	return (float( ov_num / (s1_num + s2_num - ov_num)))

#ML Estimator 3 -> Likelihood ratio
def est_3(R, s1, s2):
	s1_num = s1.number_of_nodes()
	s2_num = s2.number_of_nodes()

	num = 0
	h = []
	for i in s1.nodes():
		for j in s2.nodes():
			if i == j:
				h.append(i)
	
	#map to 0..(s1_num-1)
	mapdict_1 = {j : i for i,j in enumerate([i for i in s1.nodes()])}
	mapdict_2 = {j : i for i,j in enumerate([i for i in s2.nodes()])}
	a1 = nx.relabel_nodes(s1, mapdict_1)
	a2 = nx.relabel_nodes(s2, mapdict_2)

	loc_1 = rumor_center(to_int(nx_graph_to_adj(a1)))
	vals_s1 = RC_values(to_int(nx_graph_to_adj(a1)), loc_1)

	loc_2 = rumor_center(to_int(nx_graph_to_adj(a2)))
	vals_s2 = RC_values(to_int(nx_graph_to_adj(a2)), loc_2)

	for i in h:
		num += vals_s1[list(mapdict_1.keys()).index(i)][1] * vals_s2[list(mapdict_2.keys()).index(i)][1]

	denom = sum([j for (i,j) in vals_s1])*sum([j for (i,j) in vals_s2]) - num

	return (R*float(num/denom))

#Estimator 4 -> Comparing rumor centers
def est_4(s1, s2):
	s1_num = s1.number_of_nodes()
	s2_num = s2.number_of_nodes()

	#map to 0..(s1_num-1)
	mapdict_1 = {j : i for i,j in enumerate([i for i in s1.nodes()])}
	mapdict_2 = {j : i for i,j in enumerate([i for i in s2.nodes()])}
	a1 = nx.relabel_nodes(s1, mapdict_1)
	a2 = nx.relabel_nodes(s2, mapdict_2)
	
	loc_1 = rumor_center(to_int(nx_graph_to_adj(a1)))
	loc_2 = rumor_center(to_int(nx_graph_to_adj(a2)))
	
	loc_1 = (list(mapdict_1.keys()))[int(loc_1)]
	loc_2 = (list(mapdict_1.keys()))[int(loc_1)]

	return (float(1 / (nx.shortest_path_length(s1, loc_1, loc_2)+1)))

#Estimator 5 -> Overlap ratio and number of leaves in the difference
def est_5(s1, s2):
	s1_num = s1.number_of_nodes()
	s2_num = s2.number_of_nodes()

	ov_num = 0
	for i in s1.nodes():
		for j in s2.nodes():
			if i == j:
				ov_num += 1
				break

	if s1_num == max(s1_num, s2_num):
		big = s1.copy()
		big.remove_nodes_from(n for n in s1 if n in s2)
	else:
		big = s2.copy()
		big.remove_nodes_from(n for n in s2 if n in s1)

	num_leaves = 0
	for i in big.nodes():
		if big.degree(i) == 1:
			num_leaves += 1

	norm = 2*max(s1_num, s2_num)

	return (float(num_leaves * ov_num / ((s1_num + s2_num - ov_num) * norm) ) )