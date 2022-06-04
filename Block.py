class Block:
    # a reference to the button of the block
    button_ref = 0
    # the displayed number
    number = 0
    coordinate = 0

    def __init__(self, button_ref, number, coordinate):
        self.button_ref = button_ref
        self.number = number
        self.coordinate = coordinate
