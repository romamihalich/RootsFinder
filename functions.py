import sympy as sp
from polynomial import Polynomial

def der(f):
    terms = f.terms[:-1]
    coefs = []
    for term in terms:
        coefs.append(term.coef * term.power)
    return Polynomial(coefs)

def lagrange(f):
    if f.coefs[0] < 0:
        f = -f
    n = f.deg
    r = -1
    for i in range(n + 1):
        if f.coefs[i] < 0:
            r = n - i
            break
    if r == -1:
        return sp.nan
    neg_min = 0
    for coef in f.coefs:
        if (coef < 0) and (coef < neg_min):
            neg_min = coef
    B = abs(neg_min)
    an = f.coefs[0]
    d = B/an
    if d == int(d):
        d = int(d)
    return 1 + sp.root(d, n - r)

def get_polys(f):
    f1 = Polynomial(list(reversed(f.coefs))) # f(1/x)
    f2 = Polynomial([-term.coef if term.power % 2 != 0 else term.coef for term in f.terms]) # f(-x)
    f3 = Polynomial([-term.coef if term.power % 2 != 0 else term.coef for term in f1.terms]) # f(-(1/x))
    return f1, f2, f3

def get_sturm_series(f):
    f1 = der(f) # f'
    series = [f, f1]
    q, r = f / f1
    while r != Polynomial.ZERO:
        series.append(-r) # add fi
        q, r = series[-2] / series[-1] # fi-1 = fi*q + r

    if series[-1].deg > 0:
        for i in range(len(series)):
            q, r = series[i] / series[-1]
            series[i] = q
    return series

def get_signs(x, series):
    series_x = [f(x) for f in series] # f(x), f1(x), ..., fn(x)
    signs = []
    for num in series_x:
        if num != 0:
            if num < 0:
                signs.append(-1)
            else:
                signs.append(1)
    return signs

def w(x, series):
    signs = get_signs(x, series)
    result = 0
    for i in range(1, len(signs)):
        if signs[i] != signs[i - 1]: 
            result += 1
    return result

def get_interval(a, b):
    return sp.Interval(a, b, True, True)

def get_result(f):
    f1, f2, f3 = get_polys(f)
    series = get_sturm_series(f)

    result = {}

    if f(0) == 0:
        result["zero"] = True

    A = lagrange(f)
    A1 = lagrange(f1) 
    if A1 != sp.nan:
        pos_rootcount = w(1/A1, series) - w(A, series)
        if pos_rootcount > 0:
            pos_interval = get_interval(1/A1, A)
            result["pos"] = (pos_rootcount, pos_interval)

    A2 = lagrange(f2) 
    A3 = lagrange(f3) 
    if A3 != sp.nan:
        neg_rootcount = w(-A2, series) - w(-(1/A3), series)
        if neg_rootcount > 0:
            neg_interval = get_interval(-A2, -(1/A3))
            result["neg"] = (neg_rootcount, neg_interval)

    return result, series

def binary_search(series, left, right, acc, roots):
    f = series[0]
    if (w(left, series) - w(right, series)) > 0:
        mid = (left + right)/2
        if f(mid) == 0:
            roots["exact roots"].append(mid)
        if ((right - left) < acc) and ((w(left, series) - w(right, series)) == 1):
            roots["approximate roots"].append(right.evalf())
            return
        binary_search(series, left, mid, acc, roots)
        binary_search(series, mid, right, acc, roots)

def find_roots(result, series, digits):
    acc = 10**(-(digits + 1))
    roots = {
        "exact roots" : [],
        "approximate roots" : []
    }
    if "zero" in result:
        roots["exact roots"].append(0)

    if "neg" in result:
        interval = result["neg"][1]
        left, right = interval.inf, interval.end
        binary_search(series, left, right, acc, roots)
    
    if "pos" in result:
        interval = result["pos"][1]
        left, right = interval.inf, interval.end
        binary_search(series, left, right, acc, roots)

    f = series[0]
    i = 0
    while i < len(roots["approximate roots"]):
        roots["approximate roots"][i] = round(roots["approximate roots"][i], digits)
        c = int(round(roots["approximate roots"][i]))
        if f(c) == 0:
            del roots["approximate roots"][i]
            roots["exact roots"].append(c)
        else: 
            i += 1
    return roots