import pandas

from traitlets import (
    HasTraits, TraitType,
    Any, Float, Int, Instance
)


# TODO: see how much faster using object as the basetype would make this 
# using traits here might be overkill
class BaseReference(HasTraits):
    frame = Instance('pandas.DataFrame', allow_none=True)
    row = Int()
    value = Any()

    def __init__(self, val=None):
        self.value = val
        super().__init__()

    def set_frame(self, f):
        self.frame = f

    def set_row(self, r):
        self.row = r


class ColumnReference(BaseReference):
    def __init__(self, col=None, off=None):
        self.column = str(col)
        self.offset = off
        self.column_pos = None
        super().__init__()

    def set(self, value):
        self.frame.values[self.y,self.x] = value

    def set_frame(self, f):
        self.frame = f
        self.column_pos = self.frame.columns.get_loc(self.column)

    def set_row(self, i):
        self.row = i
        self.x = self.column_pos
        self.y = self.row + self.offset
        #TODO: look for index errors?
        self.value = self.frame.values[self.y,self.x]


class IntReference(BaseReference):
    value = Int()


class FloatReference(BaseReference):
    value = Float()


class Reference(TraitType):
    default_value = (None, 0)
    info_text = 'tuple (column name, offset)'

    def validate(self, obj, value):
        if value is None:
            return None
        if isinstance(value, int):
            return IntReference(val=value)
        if isinstance(value, float):
            return FloatReference(val=value)
        if isinstance(value, str):
            return ColumnReference(col=value, off=0)
        if isinstance(value, tuple):
            if len(value) == 2:
                if value[0] is None:
                    return None
                if isinstance(value[0], str) and isinstance(value[1], int):
                    return ColumnReference(col=value[0], off=value[1])
        self.error(obj, value)

