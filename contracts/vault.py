import smartpy as sp

from contracts.utils import Utils

class ErrorMessage: 
    NOT_ADMIN = "{}NOT_ADMIN"


class Vault(sp.Contract):
    def __init__(self, administrator):
        self.init_type(sp.TRecord(administrator=sp.TAddress))
        self.init(**self.get_initial_storage(administrator))


    @sp.entry_point
    def update_administrator(self, new_administrator): 
          sp.set_type(new_administrator, sp.TAddress)
          sp.verify(sp.sender == self.data.administrator, message=ErrorMessage.NOT_ADMIN)
          self.data.administrator = new_administrator

    def get_initial_storage(self, administrator):
        storage = {}
        storage['administrator'] = administrator
        return storage
        
@sp.add_test(name="Vault")
def test():
    scenario = sp.test_scenario()
    administrator = sp.test_account("Administrator")
    alice = sp.test_account("Alice")

    vault = Vault(administrator.address)
    scenario += vault

    scenario.verify(vault.data.administrator == administrator.address)
    
    scenario += vault.update_administrator(alice.address).run(sender=alice.address, valid = False, exception=ErrorMessage.NOT_ADMIN)
    scenario += vault.update_administrator(alice.address).run(sender=administrator.address)

    scenario.verify(vault.data.administrator == alice.address)

sp.add_compilation_target("vault", Vault(sp.address("tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU")))
