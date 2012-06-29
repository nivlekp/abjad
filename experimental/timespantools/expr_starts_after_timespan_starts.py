def expr_starts_after_timespan_starts():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression happens during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_starts_after_timespan_starts()
        TimespanInequality('t.start < expr.start')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequality('t.start < expr.start')

