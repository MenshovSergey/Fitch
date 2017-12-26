# Fitch

This program have 4 parameters:

    target:        
        fitch = create minimal convex coloring for tree. Input graph with colors on all leaves
        calc = calculate colorings of 3 types: F, G, H (see artucle). Input graph in any format (see possible format)
        brute = calculate all possible convex colorings by brute force method
        calc_network_cactus = calculate convex colorings for network and cactus using F,G,H (see article). It is more faster then brute
    format:
        CE = edge vertex and colors of vertex. First line m (count edges), n (count vertex), c (count vertex has color). m lines (a b) a->b, 
            empty line, c lines (a color)
        E = only edge vertex without colors
        N = extended newick format or newick format
    draw:
        True = if need draw input graph. In the case of fitch, will be draw graph after every step (about 2 step see article)
        False = nothing draw
    name:
        name of input file