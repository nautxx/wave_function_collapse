class Cell:
    def __init__(self, options):
        self.collapsed = False
        
        if isinstance(options, list):
            self.options = options
        else:
            self.options = list(range(options))