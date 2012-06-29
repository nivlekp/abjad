def expr_stops_during_timespan():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression stops during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_stops_during_timespan()
        TimespanInequality('t.start < expr.stop <= t.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequality('t.start < expr.stop <= t.stop')
