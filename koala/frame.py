import pandas

from traitlets.config.configurable import Configurable
from traitlets import (Instance, List)

class WrappedDataFrame(Configurable):
    _df = Instance(pandas.DataFrame, allow_none=True)
    computations = List(config=True)
    wrapping = False

    def __init__(self, **kwargs):
        self.__dict__.update(dict(
            _df = None,
            computations = [],
            wrapping = False,
        ))

        super().__init__(**kwargs)
        if self._df is not None:
            self.wrapping = True

    @classmethod
    def wrap(cls, frame):
        return cls(_df=frame)

    def unwrap(self):
        return self._df

    def _wrapping(self):
        # be very very certain that we're wrapping an object
        if 'wrapping' in self.__dict__ and self.__dict__['wrapping'] and '_df' in self.__dict__ and self._df is not None:
            return True
        return False


    #
    # Additional functionality
    #

    def extend(self, count):
        nix = pandas.tseries.index.DatetimeIndex(
            start=self._df.index[0], 
            freq=self._df.index.freqstr,
            periods=len(self._df.index)+count
        )
        self._df = self._df.reindex(nix)

    def recompute(self, offset=0):
        # make sure that self._df has a column for each computation
        targets = [getattr(c, 'target').column for c in self.computations]
        missing = [c for c in targets if c not in self._df]
        for c in missing:
            self._df[c] = pandas.Series(0, index=self._df.index)
        [c(self._df, offset=offset) for c in self.computations]


    #
    # Trait callbacks
    #

    def __df_changed(self):
        print('changed')

    def _computations_changed(self):
        pass


    #
    # Attributes
    #

    def __delattr__(self, attr):
        if self._wrapping():
            if attr not in self.__dict__:
                return delattr(self._df, attr)
        raise NotImplementedError('Cannot delete "%s" from "%s"' % (attr, self))

    def __getattr__(self, attr):
        if self._wrapping():
            if attr not in self.__dict__:
                return getattr(self._df, attr)
        return object.__getattr__(self, attr)

#    def __getattribute__(self, attr):
#        return object.__getattribute__(self, attr)

    def __setattr__(self, attr, val):
        if self._wrapping():
            if attr not in self.__dict__:
                return setattr(self._df, attr, val)
        return object.__setattr__(self, attr, val)


    #
    # Sequences
    #

    def __len__(self):
        return self._df.__len__()
    def __getitem__(self, key):
        return self._df[key]
    def __setitem__(self, key, value):
        self._df[key] = value
    def __delitem__(self, key):
        del self._df[key]
    def __iter__(self):
        return self._df.__iter__()
    def __reversed__(self):
        return self._df.__reversed__()
    def __contains__(self, item):
        return self._df.__contains__(item)
    def __missing__(self, key):
        return self._df.__missing__(key)

    #
    # Comparisons
    #

    #TODO: these need to recognize other WrappedDataFrames
    def __cmp__(self, other):
        return self._df.__cmp__(other)
    def __eq__(self, other):
        return self._df.__eq__(other)
    def __ne__(self, other):
        return self._df.__ne__(other)
    def __lt__(self, other):
        return self._df.__lt__(other)
    def __gt__(self, other):
        return self._df.__gt__(other)
    def __le__(self, other):
        return self._df.__le__(other)
    def __ge__(self, other):
        return self._df.__ge__(other)


    #
    # Representation
    #
    def __str__(self):
        if self._wrapping():
            return self._df.__str__()
        return object.__str__(self)
    def __repr__(self):
        if self._wrapping():
            return self._df.__repr__()
        return object.__repr__(self)
    def __unicode__(self):
        if self._wrapping():
            return self._df.__unicode__()
        return object.__unicode__(self)
    def __format__(self, formatstr):
        if self._wrapping():
            return self._df.__format__()
        return object.__format__(self)
    def __hash__(self):
        pass
        if self._wrapping():
            return self._df.__hash__()
        return object.__hash__(self)
    def __nonzero__(self):
        pass
        if self._wrapping():
            return self._df.__nonzero__()
        return False
    def __dir__(self):
        pass
        if self._wrapping():
            d = self._df.__dir__()
            d.extend(object.__dir__(self))
            return d
        return object.__dir__(self)
    def __sizeof__(self):
        pass
        if self._wrapping():
            return self._df.__sizeof__()
        return object.__sizeof__(self)

