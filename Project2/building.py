class Building:

    """
    Types: [Work, School, Shop, Other]
    """

    def __init__(self, pos, _type, tightness):
        self.pos = pos
        self._type = _type
        self.tightness = tightness  # Scaling parameter for infection spread since building is just 1 point.

