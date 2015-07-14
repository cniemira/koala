import os, sys
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

class TestMath(TestCase):
    def setUp(self):
        print()

    def test_00_add_add(self):
        f = Add('GROSS_PROFIT', equals='REVENUE', plus='COST_OF_REVENUE') + df
        assert 'GROSS_PROFIT' in f
        assert f['GROSS_PROFIT'][0] == 15

    def test_00_add_subtract(self):
        f = Subtract('GROSS_PROFIT', equals='REVENUE', minus='COST_OF_REVENUE') + df
        assert 'GROSS_PROFIT' in f
        assert f['GROSS_PROFIT'][0] == 5

    def test_00_add_multiply(self):
        f = Multiply('GROSS_PROFIT', equals='REVENUE', times='COST_OF_REVENUE') + df
        assert 'GROSS_PROFIT' in f
        assert f['GROSS_PROFIT'][0] == 50

    def test_00_add_divide(self):
        f = Divide('GROSS_PROFIT', equals='REVENUE', divided_by='COST_OF_REVENUE') + df
        assert 'GROSS_PROFIT' in f
        assert f['GROSS_PROFIT'][0] == 2

    def test_00_plusequals_subtract(self):
        f = df.copy()
        f += Subtract('GROSS_PROFIT', equals='REVENUE', minus='COST_OF_REVENUE')
        assert 'GROSS_PROFIT' in f
        assert f['GROSS_PROFIT'][0] == 5

    def test_01_monkey_patch(self):
        f = df + Subtract('GROSS_PROFIT', equals='REVENUE', minus='COST_OF_REVENUE')
        assert 'GROSS_PROFIT' in f
        assert f['GROSS_PROFIT'][0] == 5

    def test_02_two_ops(self):
        f = df + Subtract('GROSS_PROFIT', equals='REVENUE', minus='COST_OF_REVENUE') + \
                 Add('RECONSTITUTED', equals='COST_OF_REVENUE', plus='GROSS_PROFIT')
        assert f['REVENUE'][0] == f['RECONSTITUTED'][0]

    def test_03_op_chain(self):
        f = df + (Subtract('GROSS_PROFIT', equals='REVENUE', minus='COST_OF_REVENUE') + \
                  Add('RECONSTITUTED', equals='COST_OF_REVENUE', plus='GROSS_PROFIT'))
        assert f['REVENUE'][0] == f['RECONSTITUTED'][0]

