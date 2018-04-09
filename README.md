# Phylogeny-Comparsion

1) task: the name of the problem to solve       
        count: find the number of convex colorings for a given tree/network;    
        check_if_convex: checks if a given coloring (partition on the set of leaves) is convex on a given tree or network. 
            If True and the graph is a tree, also returns the corresponding minimal coloring of internal vertices.
            
Example:

    --task=count

2) input_graph: name of the input graph file

Example:

    --input_graph=test.tree

3) input_coloring: name of the input coloring file

Example:

	--input_coloring=coloring.txt

2) input_type:

	Format of a graph:
	
		E: list of edges: First line m (number of edges), n (number of vertex), then m lines (a b) a->b;
		
		N: Newick (or extended Newick) format.
        Format of a coloring:
		L:  C (number of colors); then list of leaves' colors  (leave, color), each in a separate line;
		
		P:  C (number of colors) lines; in the i-th line - a comma separated list of leaves having the i-th color
		
Possible values: EL, EP, NL, NP (if task=check_if_convex); E, N (if task = count).

Example:

    --input_type = EP

5) draw (optional, =False by default):

    if True, draw the input graph (with colored leaves, if given)
    
Example:
 
	--draw=True

Example 1:
 
    python3 main.py --task=check_if_convex --input_graph=test2 --input_coloring=test2_coloring_l --input_type=EL --draw=True

Check if the coloring, given in =test2_coloring_l, is convex on the tree given in test2 (as a list of edges), and draw the tree with the colored leaves.

Example 2:

     python3 main.py --task=check_if_convex --input_graph=test2 --input_coloring=test2_coloring_p --input_type=EP --draw=True

Same as example 1, but difference in coloring format

Example 3:

    python3 main.py --task=count --input_graph=test.tree --input_type=N

Count all the convex colorings on each network given in test.tree (in the eNewick format).


