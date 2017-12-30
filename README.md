# Fitch

This program have 4 parameters:

    target:        
        is_convex_tree = check if a given coloring (partition on the set of leaves) is convex on a given tree (upgraded Fitch's algorithm)
            if convex, for every vertex find color
        calc = find the number of convex colorings for a given tree. 
        brute = calculate all possible convex colorings by brute force method
        calc_network_cactus = find the number of convex colorings for a given cactus network.
            It is more faster then brute
    input:
        Format for graph: First line m (count edges), n (count vertex),  m lines (a b) a->b.
        Format for coloring:
            1) C (count colors), in every line (line equals count of leaves) (a, color)
            2) C (count colors) lines, on i lines list of vertex number, which has i-th color
        CE = graph + 1 type of coloring
        CDE = graph + 2 type of coloring
        E = only edge vertex without colors
        N = extended newick format for network
    draw:
        True = if need draw input graph. In the case of fitch, will be draw graph after every step
            (about 2 step see article)
        False = nothing draw
    name:
        name of input file

Run example

    python3 --target=calc --format=CE --draw=True --name=test2