from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.timespantools.SingleSourceTimespan import SingleSourceTimespan


class ScopedValue(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, value, timespan=None):
        assert isinstance(timespan, (SingleSourceTimespan, type(None)))
        self.value = value
        self.timespan = timespan 
