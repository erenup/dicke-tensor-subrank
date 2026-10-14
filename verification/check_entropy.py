#!/usr/bin/env python3
"""Exact supporting checks only; the all-multiplicity result uses the written proof."""
from collections import Counter
from itertools import permutations, combinations
from math import gcd, prod
import json


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def expect_rejection(label, callback):
    try:
        callback()
    except SystemExit as exc:
        require(exc.code != 0, 'negative control used a successful exit: '+label)
        return
    raise SystemExit('negative control was accepted: '+label)


def primitive(v):
    g=0
    for a in v:
        g=gcd(g,abs(a))
    if not g:
        return None
    w=tuple(a//g for a in v)
    return w if next(a for a in w if a) > 0 else tuple(-a for a in w)


def cross(u,v):
    return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])


def dot(u,v):
    return sum(a*b for a,b in zip(u,v))


def quotient_key(s,kind,v):
    u=s[1:-1]
    if kind == 'full':
        return (s[0],)
    if kind == 'plane':
        return (s[0],dot(u,v))
    pivot=next(i for i,a in enumerate(v) if a)
    return (s[0],)+tuple(u[i]*v[pivot]-u[pivot]*v[i] for i in range(len(u)) if i != pivot)


def contains_difference(a,b,kind,v):
    if a[0] != b[0]:
        return False
    u=tuple(x-y for x,y in zip(a[1:-1],b[1:-1]))
    if kind == 'full':
        return True
    if kind == 'plane':
        return dot(u,v)==0
    return primitive(u) in (None,v)


def exact_inequality(ds,fiber_product,r):
    k=sum(ds)
    # M is supplied independently from the actual permutation support.
    values=[]
    for label,multiplicity in enumerate(ds):
        values.extend([label]*multiplicity)
    M=len(set(permutations(values)))
    # (1/M) log(A) <= r/(k-2) [log(M)-H(ds/k)].
    lhs=pow(fiber_product,k*(k-2))*pow(k,k*M*r)
    rhs=pow(M,k*M*r)*pow(prod(pow(a,a) for a in ds),M*r)
    return lhs <= rhs,lhs == rhs


def validate_inequality(ds,fiber_product,r):
    good,equal=exact_inequality(ds,fiber_product,r)
    require(good, f'failed entropy/rank inequality: d={ds}, claimed rank={r}')
    return equal


def check(ds):
    k=sum(ds)
    dimension=k-2
    require(1 <= dimension <= 3, 'supporting checker dimension out of scope')
    values=[]
    for label,multiplicity in enumerate(ds):
        values.extend([label]*multiplicity)
    S=sorted(set(permutations(values)))
    lines=set()
    for a,b in combinations(S,2):
        if a[0]==b[0]:
            v=primitive(tuple(x-y for x,y in zip(a[1:-1],b[1:-1])))
            if v:
                lines.add(v)
    subspaces=[]
    if dimension >= 2:
        subspaces.extend(('line',v,1) for v in sorted(lines))
    if dimension == 3:
        planes={primitive(cross(u,v)) for u,v in combinations(lines,2)}-{None}
        subspaces.extend(('plane',v,2) for v in sorted(planes))
    subspaces.append(('full',None,dimension))
    equalities=0
    for kind,v,r in subspaces:
        keys=[quotient_key(s,kind,v) for s in S]
        counts=Counter(keys)
        A=prod(counts[key] for key in keys)
        # Independent membership calculation checks every fiber before using it.
        for a,key in zip(S,keys):
            actual=sum(contains_difference(a,b,kind,v) for b in S)
            require(actual==counts[key], 'quotient class/membership mismatch')
        equal=validate_inequality(ds,A,r)
        equalities+=int(equal)
    full_keys=[quotient_key(s,'full',None) for s in S]
    counts=Counter(full_keys)
    full_A=prod(counts[x] for x in full_keys)
    expect_rejection('lowered full-space rank',
                     lambda:validate_inequality(ds,full_A,dimension-1))
    return {'d':ds,'support_size':len(S),'nonzero_collision_subspaces':len(subspaces),
            'equalities':equalities,'wrong_rank_negative_control':'REJECTED',
            'all_fibers_independently_checked':True}


if __name__=='__main__':
    print(json.dumps({'scope':'Finite supporting checks; not the all-d proof',
                      'arithmetic':'exact integers only',
                      'cases':[check(ds) for ds in ((1,1,1),(2,1,1),(1,1,1,1),(2,2,1),(3,1,1))]},sort_keys=True,indent=2))
