import pandas

from traitlets import HasTraits

from .refs import Reference

class MathematicalOperation(HasTraits):
    target = Reference()

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

    def __call__(self, frame, offset=0):
        assert isinstance(frame, pandas.DataFrame)

        # get the attrs
        attrs = [getattr(self, a) for a in self.class_trait_names()]
        [a.set_frame(frame) for a in attrs]
    
        assert offset < frame.values.shape[0]
        end = frame.values.shape[0]
        for i in range(offset, end):
            [a.set_row(i) for a in attrs]
            self.solve(frame.values, i)


class Add(MathematicalOperation):
    augend = Reference(alias=['a', 'equals'], require=True)
    addend = Reference(alias=['d', 'plus'], require=True)

    def solve(self, arr, off):
        self.target.set(self.augend.value + self.addend.value)


class Divide(MathematicalOperation):
    dividend = Reference(alias=['d', 'equals'], require=True)
    divisor = Reference(alias=['v', 'divided_by'], require=True)

    def solve(self, arr, off):
        self.target.set(self.dividend.value / self.divisor.value)


class Multiply(MathematicalOperation):
    multiplicand = Reference(alias=['m', 'equals'], require=True)
    multiplier = Reference(alias=['r', 'multiplied_by', 'times'], require=True)

    def solve(self, arr, off):
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

    def solve(self, arr, off):
        self.target.set(self.minuend.value - self.subtrahend.value)

