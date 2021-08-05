import smartpy as sp

class Viewer(sp.Contract):
    def __init__(self):
        self.init(address=sp.address("tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU"))

    @sp.entry_point
    def set_address(self, address):
        sp.set_type_expr(address, sp.TAddress)
        self.data.address = address
