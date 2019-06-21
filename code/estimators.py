#Estimator 1 -> s1^s2 / s1*s2 - s1^s2
def est_1(G, s1, s2):
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

#Estimator 2 -> s1^s2 / min(s1,s2)
def est_2(G, s1, s2):
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