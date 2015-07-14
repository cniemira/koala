import pandas

from traitlets import HasTraits, Int

from .refs import Reference

class MathematicalOperation(HasTraits):
    target = Reference()
    offset = Int(default_value=0)

    def __init__(self, target, **kwargs):
        super().__init__(**kwargs)

        # target gets explicitly set 
        self.target = target

        # allow aliases
        for attr,trait in self.class_traits().items():
            alias = trait.get_metadata('alias')
            if isinstance(alias, str):
                alias = [alias]
            if isinstance(alias, list):
                for a in alias:
                    if hasattr(self, a):
                        setattr(self, attr, getattr(self, a))

            if trait.get_metadata('require'):
                if not bool(getattr(self, attr)):
                    raise AttributeError('Missing required attribute: "%s"' %
                            (attr))

    def __add__(self, obj):
        return self._do_add(obj)

    def __iadd__(self, obj):
        return self._do_add(obj)

    def __radd__(self, obj):
        return self._do_add(obj)

    def _do_add(self, obj):
        if isinstance(obj, pandas.DataFrame):
            return self(obj, offset=self.offset)
        #todo: sequence
        if isinstance(obj, MathematicalOperation):
            return OperationChain(self, obj)
        #todo: sequence
        if isinstance(obj, OperationChain):
            return obj.append(self)

        raise NotImplementedError()

    def __call__(self, frame, offset=None):
        assert isinstance(frame, pandas.DataFrame)

        offset = offset or self.offset
        assert offset < frame.values.shape[0]

        # get the refs
        refs = [getattr(self, a) for a,t in self.class_traits().items() if type(t) is Reference]

        # make sure the target column exists
        if self.target.column not in frame.index:
            frame[self.target.column] = pandas.Series(0, index=frame.index)

        [a.set_frame(frame) for a in refs]
        end = frame.values.shape[0]
        for i in range(offset, end):
            [a.set_row(i) for a in refs]
            self.solve()

        return frame


class OperationChain(object):
    def __init__(self, *args):
        self.ops = []
        for op in args:
            assert isinstance(op, MathematicalOperation)
            self.ops.append(op)

    def __add__(self, frame):
        assert isinstance(frame, pandas.DataFrame)
        for op in self.ops:
            frame += op
        return frame

    def __radd__(self, frame):
        assert isinstance(frame, pandas.DataFrame)
        for op in self.ops:
            frame += op
        return frame

    def append(self, op):
        assert isinstance(op, MathematicalOperation)
        self.ops.append(op)
        return self


class Add(MathematicalOperation):
    augend = Reference(alias=['a', 'equals'], require=True)
    addend = Reference(alias=['d', 'plus'], require=True)

    def solve(self):
        self.target.set(self.augend.value + self.addend.value)


class Divide(MathematicalOperation):
    dividend = Reference(alias=['d', 'equals'], require=True)
    divisor = Reference(alias=['v', 'divided_by'], require=True)

    def solve(self):
        self.target.set(self.dividend.value / self.divisor.value)


class Multiply(MathematicalOperation):
    multiplicand = Reference(alias=['m', 'equals'], require=True)
    multiplier = Reference(alias=['r', 'multiplied_by', 'times'], require=True)

    def solve(self):
        self.target.set(self.multiplicand.value * self.multiplier.value)


class Subtract(MathematicalOperation):
    # Creates a subtraction call
    #
    # Args:
    #   m (Reference):  minuend
    #   s (Reference):  subtrahend
    #
    #   Arguments can take any form valid for a Reference object
    #
    minuend = Reference(alias=['m', 'equals'], require=True)
    subtrahend = Reference(alias=['s', 'minus', 'less'], require=True)

    def solve(self):
        self.target.set(self.minuend.value - self.subtrahend.value)


# I feel dirty...
_pandas_add = pandas.DataFrame.__add__

def _monkey_add(self, other):
    if isinstance(other, (MathematicalOperation, OperationChain)):
        return other.__radd__(self)
    return _pandas_add(self, other)

pandas.DataFrame.__add__ = _monkey_add
pandas.DataFrame.__iadd__ = _monkey_add
pandas.DataFrame.__radd__ = _monkey_add

