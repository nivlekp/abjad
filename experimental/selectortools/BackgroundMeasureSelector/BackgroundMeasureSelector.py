from experimental.selectortools.BackgroundElementSelector import BackgroundElementSelector


class BackgroundMeasureSelector(BackgroundElementSelector):
    r'''.. versionadded:: 1.0


    ::

        >>> from experimental import selectortools
        >>> from experimental import timespantools

    Select measure ``3`` in score::

        >>> selectortools.BackgroundMeasureSelector(index=3)
        BackgroundMeasureSelector(index=3)

    Select the last measure to start in the first third of the score::


        >>> timespan = timespantools.SingleSourceTimespan(multiplier=Fraction(1, 3))
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> selector = selectortools.BackgroundMeasureSelector(inequality=inequality, index=-1)

    ::
    
        >>> z(selector)
        selectortools.BackgroundMeasureSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    multiplier=Fraction(1, 3)
                    )
                ),
            index=-1
            )

    Select the first measure starting during segment ``'red'``::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)

    ::

        >>> selector = selectortools.BackgroundMeasureSelector(inequality=inequality)

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureSelector(
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            index=0
            )

    Measure selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, index=0):
        from abjad.tools import measuretools
        BackgroundElementSelector.__init__(
            self, klass=measuretools.Measure, index=index, inequality=inequality)
