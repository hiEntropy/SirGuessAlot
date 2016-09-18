class Segment:
    type_ = None
    count = None

    def __init__(self, type_, count):
        if type_ in ['n', 'l', 's', 'u']:
            self.type_ = type_
        self.count = count
