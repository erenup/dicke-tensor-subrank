#!/usr/bin/env python3
"""Exact finite checks of new hashing proof; does not certify general theorem."""
import itertools
import json
from collections import Counter
from fractions import Fraction


def need(ok, message):
    if not ok:
        raise SystemExit(message)


def expect_rejection(label, callback):
    try:
        callback()
    except SystemExit as exc:
        need(exc.code != 0, 'negative control used a successful exit: '+label)
        return label
    raise SystemExit('negative control was accepted: '+label)


def validate_average_free(B,q):
    need(all((x+y-2*z)%q != 0 or x==y==z for x in B for y in B for z in B),
         'average-free condition violated')


def validate_induced_restriction(candidates, original):
    if not candidates:
        return
    k=len(next(iter(candidates)))
    kept=[{x[i] for x in candidates} for i in range(k)]
    need({x for x in original if all(x[i] in kept[i] for i in range(k))}==candidates,
         'noncandidate mixed edge remains in restriction')


def support(d):
    return sorted(set(itertools.permutations(tuple(a for a,m in enumerate(d) for _ in range(m)))))


def canonical_line(v):
    from math import gcd
    g=0
    for x in v: g=gcd(g, abs(x))
    if not g: return None
    v=tuple(x//g for x in v)
    if next(x for x in v if x) < 0: v=tuple(-x for x in v)
    return v


def on_line(v, u):
    pivot=next(i for i,x in enumerate(u) if x)
    return all(v[i]*u[pivot]==v[pivot]*u[i] for i in range(len(v)))


def check_fibers(d):
    S=support(d); k=sum(d); M=len(S)
    need(all((M*a)%k==0 for a in d), 'nonintegral marginal count')
    nlines=0
    for j in range(k):
        lines={canonical_line(tuple(x-y for x,y in zip(a,b)))
               for a in S for b in S if a[j]==b[j]}
        lines.discard(None)
        for u in lines:
            product=1
            for a in S:
                count=sum(on_line(tuple(x-y for x,y in zip(b,a)),u) for b in S)
                product*=count
            rhs=Fraction(M**M)
            for a in d: rhs*=Fraction(a,k)**(M*a//k)
            need(Fraction(product**(k-2))<=rhs, 'rank-one fiber entropy bound failed')
            nlines+=1
    return {'d':d,'support':M,'rank_one_subspaces_with_mode_multiplicity':nlines}


def test_hash():
    k=3; N=3; q=11; B={0,1,3}
    validate_average_free(B,q)
    S=((-1,-1,2),(-1,2,-1),(2,-1,-1))
    edges=[]; candidate=[]
    for cols in itertools.product(S,repeat=N):
        edges.append(tuple(tuple(c[j] for c in cols) for j in range(k)))
        candidate.append(len(set(cols))==3)
    need(sum(candidate)==6,'candidate count')
    pair_list=[(i,j) for i,I in enumerate(edges) if candidate[i]
               for j,J in enumerate(edges) if j!=i and any(I[z]==J[z] for z in range(k))]
    need(len(pair_list)==54,'pair count')
    hit=[0]*len(edges); pair_hit=Counter(); total_X=total_Y=total_isolated=0
    max_matching=0; assignments=q**(N+k-1)
    inv2=pow(2,-1,q)
    for v in itertools.product(range(q),repeat=N):
        dots={w:sum(x*y for x,y in zip(w,v))%q for I in edges for w in I}
        for u in itertools.product(range(q),repeat=k-1):
            survivors=[]
            for i,I in enumerate(edges):
                hashes=((u[0]+dots[I[0]])%q,(u[1]+dots[I[1]])%q,((u[0]+u[1]-dots[I[2]])*inv2)%q)
                if all(h in B for h in hashes):
                    need(len(set(hashes))==1,'average-free filter did not force equal hashes')
                    survivors.append(i); hit[i]+=1
            surv=set(survivors)
            pairs=[(i,j) for i,j in pair_list if i in surv and j in surv]
            for pair in pairs: pair_hit[pair]+=1
            candidates=[i for i in survivors if candidate[i]]
            isolated=[i for i in candidates if not any(a==i for a,b in pairs)]
            need(len(isolated)>=len(candidates)-len(pairs),'isolated-candidate deletion bound')
            # Check final restriction in FULL original support, not just survivors.
            validate_induced_restriction({edges[i] for i in isolated}, set(edges))
            total_X+=len(candidates); total_Y+=len(pairs); total_isolated+=len(isolated)
            max_matching=max(max_matching,len(isolated))
    expected_candidate=q**N*len(B)
    need(all(hit[i]==expected_candidate for i in range(len(edges))),'single-edge probability')
    expected_pair=q**(N-1)*len(B)
    need(all(pair_hit[pair]==expected_pair for pair in pair_list),'pair-rank probability')
    need(total_X>total_Y,'finite positive-expectation control')
    return {'q':q,'B':sorted(B),'assignments':assignments,'edges':len(edges),'candidates':sum(candidate),
            'candidate_collider_pairs':len(pair_list),'single_hits':expected_candidate,'pair_hits':expected_pair,
            'sum_X':total_X,'sum_Y':total_Y,'sum_isolated':total_isolated,'max_isolated_matching':max_matching}


def controls():
    # The invariance hypothesis is essential: supported on one line in Q^2,
    # F(line)=log 2 > (1/2)H(X). Integer exponent version: 2^2 > 2.
    out=[expect_rejection('noninvariant_entropy_bound_rejected',
                          lambda:need(2**2<=2,'entropy slope claim fails without invariance'))]
    # Average-free hypothesis is essential: 0+2=2*1 has unequal entries.
    out.append(expect_rejection('non_average_free_B_rejected',
                                lambda:validate_average_free({0,1,2},11)))
    # Candidate isolation must include all edges, not just candidates:
    # diagonal candidates (0,0),(1,1) alone look induced, but a hidden (0,1)
    # edge survives the local vertices from both candidates.
    candidates={(0,0),(1,1)}; original=candidates|{(0,1)}
    out.append(expect_rejection('candidate_only_isolation_rejected',
                                lambda:validate_induced_restriction(candidates,original)))
    return out


if __name__=='__main__':
    result={'scope':'finite exact supporting checks, not a proof of all multiplicities',
            'fiber_checks':[check_fibers(d) for d in [(2,1),(1,1,1),(2,2),(2,1,1),(1,1,1,1),(3,1,1),(2,2,1)]],
            'hash_check':test_hash(),'negative_controls':controls()}
    print(json.dumps(result,sort_keys=True,indent=2))
