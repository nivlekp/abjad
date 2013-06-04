from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuToken(list, AbjadObject):
    '''Menu token.

    Return menu token.
    '''

    ### CLASS VARIABLES ###

    return_value_attributes = ('body', 'key', 'number', 'prepopulated')

    ### INITIALIZER ###

    def __init__(self, expr, number=None, return_value_attribute=None):
        if isinstance(expr, str):
            self.append(expr)
        elif isinstance(expr, (tuple, type(self))):
            assert 1 <= len(expr) <= 4, repr(expr)
            for x in expr:
                self.append(x)
        else:
            raise TypeError(expr)
        self._number = number
        assert return_value_attribute in self.return_value_attributes, repr(return_value_attribute)
        self._return_value_attribute = return_value_attribute
        prepopulated_return_value = None
        if len(self) == 1:
            key, body, existing_value = None, self[0], None
            return_value = self[0]
        elif len(self) == 2:
            key, body, existing_value = self[0], self[1], None
        elif len(self) == 3:
            key, body, existing_value = self
        elif len(self) == 4:
            key, body, existing_value, prepopulated_return_value = self
        self._key = key
        self._body = body
        self._existing_value = existing_value
        self._prepopulated_return_value = prepopulated_return_value
        if len(self) == 1:
            return_value = self[0]
        elif self.return_value_attribute == 'key':
            return_value = self[0]
        elif self.return_value_attribute == 'body':
            return_value = self[1]
        elif self.return_value_attribute == 'number':
            return_value = None
        elif self.return_value_attribute == 'prepopulated':
            return_value = self[3]
        self._return_value = return_value

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({})'.format(self._class_name, ', '.join([repr(x) for x in self]))

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def body(self):
        return self._body

    @property
    def existing_value(self):
        return self._existing_value

    @property
    def key(self):
        return self._key

    @property
    def number(self):
        return self._number

    @property
    def prepopulated_return_value(self):
        return self._prepopulated_return_value

    # TODO: harmonize this implementation with that in MenuSection.unpack_menu_tokens()
    @property
    def return_value(self):
        return self._return_value

    @property
    def return_value_attribute(self):
        return self._return_value_attribute
