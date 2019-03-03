from .scores import Scores


class BaseAbility(object):

    def __init__(self, scores: Scores):
        super(BaseAbility, self).__init__()
        self.scores = scores
