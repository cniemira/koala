import os
from unittest import TestCase

import nose.tools
import pandas

from . import (
    WrappedDataFrame,
    Add, Subtract, Multiply, Divide
)

df = pandas.DataFrame(
    [[10,5],
     [20,6]],
    columns=['REVENUE', 'COST_OF_REVENUE'],
    index=pandas.DatetimeIndex(start='2015-01-01', freq='d', periods=2)
)

class TestWrappedDataFrame(TestCase):
    def setUp(self):
        print()

    def test_01_wrap(self):
        f = WrappedDataFrame.wrap(df)
        assert 'REVENUE' in f

    def test_01_unwrap(self):
        f = WrappedDataFrame.wrap(df)
        df2 = f.unwrap()
        assert id(df2) == id(df)

    def test_02_dir(self):
        f = WrappedDataFrame.wrap(df)
        d = dir(f)
        assert 'recompute' in d
        assert 'to_panel' in d

    def test_03_extend(self):
        f = WrappedDataFrame.wrap(df)
        assert len(f) == 2
        f.extend(3)
        assert len(f) == 5

    def test_03_computations(self):
        f = WrappedDataFrame.wrap(df)
        f.computations = [
            Subtract('GROSS_PROFIT', minuend='REVENUE', subtrahend='COST_OF_REVENUE'),
        ]
        f.recompute()
        assert f['GROSS_PROFIT'][0] == 5
        assert f['GROSS_PROFIT'][1] == 14

