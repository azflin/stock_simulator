"""
scripts.py is intended to be run as a script from the command line. Currently it contains
code to force margin calls for all portfolios that carry too much short exposure.
"""

from models import Portfolio


def force_margin_call(portfolio):
    raise NotImplementedError


if __name__ == "__main__":
    portfolios = Portfolio.objects.all()
    for p in portfolios:
        force_margin_call(p)
