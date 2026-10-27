"""Exact synthetic flow accounting; never infer joint measured traffic this way."""
from fractions import Fraction
from functools import reduce
from operator import mul


def product(values):
    return reduce(mul, values, Fraction(1))


def independent_flows(model):
    """Return stage shares, eligible shares, fast-path total, and pairwise links.

    The caller must explicitly select an illustrative, independent model. Each
    node needs a positive weight and a Boolean eligibility flag. The fast cohort
    satisfies eligibility in every layer, not just one adjacent pair.
    """
    if model.get('kind') != 'illustrative' or model.get('mix_assumption') != 'independent':
        raise ValueError('This helper requires an explicit illustrative independent mix.')
    layers=model['layers']
    if len(layers)<2:
        raise ValueError('At least two layers are required.')
    for layer in layers:
        if not layer['nodes'] or any(n['weight']<=0 or type(n['eligible']) is not bool for n in layer['nodes']):
            raise ValueError('Every node needs a positive weight and Boolean eligibility.')
    shares=[[Fraction(n['weight'])/sum(Fraction(n['weight']) for n in layer['nodes']) for n in layer['nodes']] for layer in layers]
    eligible=[sum(p for p,n in zip(ps,layer['nodes']) if n['eligible']) for ps,layer in zip(shares,layers)]
    fast_total=product(eligible)
    links=[]
    for k in range(len(layers)-1):
        rest=product(p for i,p in enumerate(eligible) if i not in (k,k+1))
        layer_links=[]
        for i,a in enumerate(layers[k]['nodes']):
            for j,b in enumerate(layers[k+1]['nodes']):
                total=shares[k][i]*shares[k+1][j]
                fast=total*rest if a['eligible'] and b['eligible'] else Fraction(0)
                layer_links.append({'source':i,'target':j,'total':total,'fast':fast,'python':total-fast})
        links.append(layer_links)
    return shares,eligible,fast_total,links
