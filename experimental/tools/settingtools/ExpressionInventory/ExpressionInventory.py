import copy
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.tools.settingtools.Expression import Expression


class ExpressionInventory(ObjectInventory, Expression):
    '''Expression inventory.

    Each expression will be evaluated in turn.
    '''
    
    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        tokens = [copy.deepcopy(x) for x in self]
        result = type(self)(tokens=tokens, name=self.name)
        return result

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _payload_elements(self):
        result = []
        for expression in self:
            result.extend(expression._payload_elements)
        return result

    ### PRIVATE METHODS ###

    def _evaluate(self):
        result = type(self)()
        for expression in self:
            expression = expression._evaluate()
            result.append(expression)
        return result
