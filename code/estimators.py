from rumor_center import *

#Estimator 0 -> s1^s2 / s1*s2 - s1^s2
def est_0(G, s1, s2):
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
def est_1(G, s1, s2):
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
def est_2(G, s1, s2):
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
def est_3(G, s1, s2):
	s1_num = s1.number_of_nodes()
	s2_num = s2.number_of_nodes()

	num = 0
	h = []
	for i in s1.nodes():
		for j in s2.nodes():
			if i == j:
				h.append(i)
	loc_1 = rumor_center(to_int(nx_graph_to_adj(s1)))
	vals_s1 = RC_values(to_int(nx_graph_to_adj(s1)), loc_1)

	loc_2 = rumor_center(to_int(nx_graph_to_adj(s2)))
	vals_s2 = RC_values(to_int(nx_graph_to_adj(s2)), loc_2)

	for i in h:
		num += vals_s1[int(i)][1] * vals_s2[int(i)][1]

	denom = sum([j for (i,j) in vals_s1])*sum([j for (i,j) in vals_s2]) - num

	return (float(num/denom))

#Estimator 4 -> Overlap ratio / number of connected components
def est_4(G, s1, s2):
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

	num_con = nx.algorithms.components.number_connected_components(big)
	return (float(num_con * ov_num / (min(s1_num, s2_num)**2) ))
