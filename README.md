Koala is python package for expressive manipulation of structured data. It aims to make data modeling more approachable. This pre-alpha version only supports pandas.DataFrame objects.

It lets you do this:
```python
df = DataFrame.from_csv('aapl.csv')
df += Subtract('GROSS_PROFIT', equals='REVENUE', minus='COSTS')
```

It also understands operation chains:
```python
ops = Subtract('GROSS_PROFIT', equals='REVENUE', minus='COSTS') + \
      Add('ASSETS', equals='LIABILITIES', plus='EQUITY')

df_aapl = DataFrame.from_csv('aapl.csv')
df_goog = DataFrame.from_csv('aapl.csv')

df_aapl += ops
df_goog += ops
```

And includes a "wrapper" around the traditional DataFrame object:
```python
df = WrappedDataFrame.wrap(DataFrame.from_csv('aapl.csv'))
df.computations = [Subtract('GROSS_PROFIT', equals='REVENUE', minus='COSTS'),
	           Add('ASSETS', equals='LIABILITIES', plus='EQUITY')]
df.recompute()
```
