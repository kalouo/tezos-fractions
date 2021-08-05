import smartpy as sp

FA2 = sp.io.import_script_from_url("file:./FA2.py")

class Vault(sp.Contract):
    def __init__(self):
        self.init_type(sp.TRecord(administrator=sp.TAddress))

    @sp.entry_point
    def deposit(self, asset_contract_address, asset_token_id):
        sp.set_type(asset_contract_address, sp.TAddress)
        sp.set_type(asset_token_id, sp.TNat)

        transfer_token_contract = sp.contract(FA2.Transfer.get_batch_type(
        ), asset_contract_address, entry_point="transfer").open_some()
        transfer_payload = [FA2.Transfer.item(sp.sender, [sp.record(
            to_=self.address, token_id=asset_token_id, amount=sp.nat(1))])]
        sp.transfer(transfer_payload, sp.mutez(0), transfer_token_contract)


@sp.add_test(name="Vault")
def test():
    pass


sp.add_compilation_target("vault", Vault(), storage=sp.record(
    administrator=sp.address("tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU")))
