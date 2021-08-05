import smartpy as sp

from contracts.utils import Utils


class Vault(sp.Contract):
    def __init__(self):
        self.init_type(sp.TRecord(administrator=sp.TAddress))

    @sp.entry_point
    def deposit(self, asset_contract_address, asset_token_id):
        sp.set_type(asset_contract_address, sp.TAddress)
        sp.set_type(asset_token_id, sp.TNat)

        Utils.execute_token_transfer(
            asset_contract_address, sp.sender, sp.self_address, asset_token_id, sp.nat(1))


@sp.add_test(name="Vault")
def test():
    pass


sp.add_compilation_target("vault", Vault(), storage=sp.record(
    administrator=sp.address("tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU")))
