import itertools
from nose.tools import assert_true
import numpy as np
from ..proximal_operators import prox_l1, prox_tvl1


def test_prox_l1_nonexpansiveness(n_features=10):
    rng = np.random.RandomState(42)
    x = rng.randn(n_features, 1)
    tau = .3
    s = prox_l1(x.copy(), tau)
    p = x - s  # projection + shrinkage = id

    # We should have ||s(a) - s(b)||^2 <= ||a - b||^2 - ||p(a) - p(b)||^2
    # for all a and b (this is strong non-expansiveness
    for (a, b), (pa, pb), (sa, sb) in zip(*[itertools.product(z[0], z[0])
                                            for z in [x, p, s]]):
        assert_true((sa - sb) ** 2 <= (a - b) ** 2 - (pa - pb) ** 2)


def test_prox_tvl1_approximates_prox_l1_for_lasso(size=15, random_state=42,
                                                   decimal=4, dgap_tol=1e-7):

    rng = np.random.RandomState(random_state)

    l1_ratio = 1.  # pure LASSO
    for ndim in xrange(3, 4):
        shape = [size] * ndim
        z = rng.randn(*shape)
        for weight in np.logspace(-10, 10, num=10):
            # use prox_tvl1 approximation to prox_l1
            a = prox_tvl1(z.copy(), weight=weight, l1_ratio=l1_ratio,
                           dgap_tol=dgap_tol, return_info=False,
                           max_iter=10,
                           )[-1].ravel()

            # use exact closed-form soft shrinkage formula for prox_l1
            b = prox_l1(z.copy(), weight)[-1].ravel()

            # results shoud be close in l-infinity norm
            np.testing.assert_almost_equal(np.abs(a - b).max(),
                                           0., decimal=decimal)


def test_proj_lpinty(p=10):
    import sys
    import os
    sys.path.append(os.path.join(os.environ["HOME"],
                                 "CODE/FORKED/parietal-python"))
    from parietal.learn.proximal.projections import proj_lpinfty
    rng = np.random.RandomState(42)
    z = np.ones((4, p))
    np.testing.assert_array_equal(_projector_on_dual(z.copy(), 0.)[:-1],
                                  proj_lpinfty(z[:-1], 1., p=2, inplace=False))
