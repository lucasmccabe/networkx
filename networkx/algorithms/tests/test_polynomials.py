"""Unit tests for the :mod:`networkx.algorithms.polynomials` module."""

import networkx as nx
import pytest

sympy = pytest.importorskip("sympy")


# Mapping of input graphs to a string representation of their tutte polynomials
_test_tutte_graphs = {
    nx.complete_graph(1): "1",
    nx.complete_graph(4): "x**3 + 3*x**2 + 4*x*y + 2*x + y**3 + 3*y**2 + 2*y",
    nx.cycle_graph(5): "x**4 + x**3 + x**2 + x + y",
    nx.diamond_graph(): "x**3 + 2*x**2 + 2*x*y + x + y**2 + y",
}

_test_chromatic_graphs = {
    nx.complete_graph(1): "x",
    nx.complete_graph(4): "x*(x**3 - 6*x**2 + 11*x - 6)",
    nx.cycle_graph(5): "((-1)**5)*(x-1)+(x-1)**5",
    nx.diamond_graph(): "x*(x**3 - 5*x**2 + 8*x - 4)",
    nx.path_graph(5): "x*(x-1)**4",
}


@pytest.mark.parametrize(("G", "expected"), _test_tutte_graphs.items())
def test_tutte_polynomial(G, expected):
    assert nx.tutte_polynomial(G).equals(expected)


@pytest.mark.parametrize("G", _test_tutte_graphs.keys())
def test_tutte_polynomial_disjoint(G):
    """Tutte polynomial factors into the Tutte polynomials of its components.
    Verify this property with the disjoint union of two copies of the input graph.
    """
    t_g = nx.tutte_polynomial(G)
    H = nx.disjoint_union(G, G)
    t_h = nx.tutte_polynomial(H)
    assert sympy.simplify(t_g * t_g).equals(t_h)


@pytest.mark.parametrize(("G", "expected"), _test_chromatic_graphs.items())
def test_chromatic_polynomial(G, expected):
    assert nx.chromatic_polynomial(G).equals(expected)


@pytest.mark.parametrize("G", _test_chromatic_graphs.keys())
def test_chromatic_polynomial_disjoint(G):
    """Chromatic polynomial factors into the Chromatic polynomials of its
    components. Verify this property with the disjoint union of two copies of
    the input graph.
    """
    x_g = nx.chromatic_polynomial(G)
    H = nx.disjoint_union(G, G)
    x_h = nx.chromatic_polynomial(H)
    assert sympy.simplify(x_g * x_g).equals(x_h)
