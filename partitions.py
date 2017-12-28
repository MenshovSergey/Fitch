__author__ = 'nikita'
import copy

def all_parts(se):
    if len(se) == 1:
        return [[[se[0]]]]
    else:
        prev, item  = se[:-1], se[-1]
        all_prev = all_parts(prev)
        res = []
        for p in all_prev:
            res.append(p+[[item]])
            for i in range(len(p)):
                pnew = copy.deepcopy(p)
                pnew[i].append(item)
                res.append(pnew)
        return res

def as_a_coloring(p):
    res = dict()
    for i in range(len(p)):
        for item in p[i]:
            res[item] = i+1
    return res
