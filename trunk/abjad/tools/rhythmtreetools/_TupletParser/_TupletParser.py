import copy
from abjad import *
from abjad.tools.mathtools import NonreducedFraction
from abjad.tools.rhythmtreetools._Parser import _Parser


class _TupletParser(_Parser):

    ### LEX SETUP ###

    tokens = (
        'BRACE_L',
        'BRACE_R',
        'COMMA',
        'DOT',
        'FRACTION',
        'INTEGER',
        'PAREN_L',
        'PAREN_R',
        'PIPE',
    )

    t_BRACE_L = '{'
    t_BRACE_R = '}'
    t_COMMA = ','
    t_DOT = '\.'
    t_PAREN_L = '\('
    t_PAREN_R = '\)'
    t_PIPE = '\|'

    t_ignore = ' \n\t\r'

    ### YACC SETUP ###

    start = 'start'

    ### LEX METHODS ###

    def t_FRACTION(self, t):
        r'(-?[1-9]\d*/[1-9]\d*)'
        parts = t.value.split('/')
        t.value = NonreducedFraction(int(parts[0]), int(parts[1]))
        return t

    def t_INTEGER(self, t):
        r'(-?[1-9]\d*)'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    ### YACC METHODS ###

    def p_component__container(self, p):
        '''component : container'''
        p[0] = p[1]

    def p_component__fixed_duration_container(self, p):
        '''component : fixed_duration_container'''
        p[0] = p[1]

    def p_component__leaf(self, p):
        '''component : leaf'''
        p[0] = p[1]

    def p_component__tuplet(self, p):
        '''component : tuplet'''
        p[0] = p[1]

    def p_component_list__EMPTY(self, p):
        '''component_list : '''
        p[0] = []

    def p_component_list__component_list__component(self, p):
        '''component_list : component_list component'''
        p[0] = p[1] + [p[2]]

    def p_container__BRACE_L__component_list__BRACE_R(self, p):
        '''container : BRACE_L component_list BRACE_R'''
        p[0] = Container()
        for component in p[2]:
            p[0].append(component)

    def p_dots__dots__DOT(self, p):
        '''dots : dots DOT'''
        p[0] = p[1] + 1

    def p_dots__EMPTY(self, p):
        '''dots : '''
        p[0] = 0

    def p_fixed_duration_container__pair(self, p):
        '''fixed_duration_container : pair'''
        p[0] = containertools.FixedDurationContainer(p[1])

    def p_leaf__INTEGER(self, p):
        '''leaf : INTEGER dots'''
        dots = '.' * p[2]
        if 0 < p[1]:
            p[0] = Note("c'{}{}".format(p[1], dots))
        else:
            p[0] = Rest('{}{}'.format(abs(p[1]), dots))

    def p_pair__PAREN_L__INTEGER__COMMA__INTEGER__PAREN_R(self, p):
        '''pair : PAREN_L INTEGER COMMA INTEGER PAREN_R'''
        p[0] = Duration(p[2], p[4])

    def p_measure__PIPE__FRACTION__component_list__PIPE(self, p):
        '''measure : PIPE FRACTION component_list PIPE'''
        p[0] = Measure(p[2].pair)
        for x in p[3]:
            p[0].append(x)

    def p_start__EMPTY(self, p):
        '''start : '''
        p[0] = []

    def p_start__start__component(self, p):
        '''start : start component'''
        p[0] = p[1] + [p[2]]

    def p_start__start__measure(self, p):
        '''start : start measure'''
        p[0] = p[1] + [p[2]]

    def p_tuplet__FRACTION__container(self, p):
        '''tuplet : FRACTION container'''
        p[0] = tuplettools.Tuplet(p[1], p[2][:])

    def p_error(self, p):
        if p:
            print("Syntax error at '%s'" % p.value)
        else:
            print("Syntax error at EOF")
