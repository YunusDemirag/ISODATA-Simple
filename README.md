# ISODATA-Simple
This is a simple implementation of the isodata algorithm, made for a university project. 
It is far from optimized, however free for use, edit & replication.

Isodata takes as input:
	kinit - inital number of clusters
	nmin - minimum number of elements per cluster
	imax - maximum number of iterations (counted at end of loop)
	dmax - max standard deviation of a cluster
	lmininit - minumum distance between two clusters
	pmax - maximum merges per iteration
	data - Your Data, structured as a list of n-dimensional tuples
	datadimensions - n
	
Isodata gives as Output
	(number of clusters, cluster centers, clusters)
	k := number of clusters | int
	cluster centers | list of k n-dimensional tuples
	clusters | list of k lists of n-dimensional tuples
	

