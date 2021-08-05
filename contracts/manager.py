import smartpy as sp

from contracts.vault import Vault
from contracts.utils import addresses
import contracts.FA2 as FA2


class LookupKey:
    """Lookup key used when looking up a vault based on the underlying asset."""
    def get_type():
        """Returns a single lookup key type, layouted
        Returns:
            sp.TRecord: lookup key type (layouted)
        """
        return sp.TRecord(contract_address=sp.TAddress, token_id=sp.TNat).layout(("contract_address", "token_id"))

    def make(contract_address, token_id):
        """Creates a typed lookup key
        Args:
            contract_address (sp.address): contract address of the underlying asset
            token_id (sp.nat): the token id
        Returns:
            sp.record: typed lookup key
        """
        return sp.set_type_expr(sp.record(contract_address=contract_address, token_id=token_id), LookupKey.get_type())


class Manager(sp.Contract):
    def __init__(self, fractions_contract):
        self.fractions_contract = fractions_contract
        self.init(**self.get_initial_storage())

    @sp.entry_point
    def create_vault(self, asset_contract, asset_token_id, contract_address_callback):
        sp.set_type(asset_contract, sp.TAddress)
        sp.set_type(asset_token_id, sp.TNat)
        # sp.set_type(contract_address_callback, sp.TContract(sp.TAddress))

        # lookup_key = LookupKey.make(asset_contract, asset_token_id)
        # sp.verify(self.data.vault_lookup_by_underlying.contains(
        #     lookup_key) == False, message="EXISTING VAULT")

        sp.create_contract(contract=Vault(), storage=sp.record(
            administrator=self.address))

        # self.data.vault_lookup_by_underlying[lookup_key] = vault_contract_address

        # vault_contract_address = sp.create_contract(Vault(self.address))

        # # # lookup_key = LookupKey.make(asset_contract, asset_token_id)
        # # # sp.verify(self.data.vault_lookup_by_underlying.contains(
        # # #     lookup_key) == False, message="EXISTING VAULT")
        # # # self.data.vault_lookup_by_underlying[lookup_key] = vault_contract_address

        # sp.transfer(vault_contract_address, sp.mutez(
        #     0), contract_address_callback)

    @sp.entry_point
    def fractionalize(self, fractions_supply):

        sp.set_type(fractions_supply, sp.TNat)

        self.execute_token_mint(
            self.data.fractions_contract,
            sp.sender,
            self.data.next_fractions_token_id,
            fractions_supply
        )

        self.data.next_fractions_token_id += 1

    def execute_token_mint(self, token_address, to_, token_id, amount):
        mint_token_contract = sp.contract(FA2.RecipientTokenAmount.get_type(
        ), token_address, entry_point='mint').open_some()
        mint_payload = FA2.RecipientTokenAmount.make(to_, token_id, amount)
        sp.transfer(mint_payload, sp.mutez(0), mint_token_contract)

    def get_initial_storage(self):
        storage = {}
        storage['next_fractions_token_id'] = 0
        storage['fractions_contract'] = self.fractions_contract

        # vault_context_type = sp.TRecord(
        #     minted=sp.TNat, fractions_token_id=sp.TNat)
        # storage['vaults'] = sp.big_map(
        #     tkey=sp.TAddress, tvalue=vault_context_type)
        # storage['vault_lookup_by_fractions_token_id'] = sp.big_map(
        #     tkey=sp.TNat, tvalue=sp.TAddress)
        # storage['vault_lookup_by_underlying'] = sp.big_map(
        #     tkey=LookupKey.get_type(), tvalue=sp.TAddress)

        return storage

    @sp.add_test(name="Manager")
    def test():
        scenario = sp.test_scenario()

        fractions = FA2.AdministrableFA2(addresses.ADMIN)
        manager = Manager(fractions_contract=fractions.address)
        token = FA2.AdministrableFA2(addresses.ADMIN)

        scenario += fractions
        scenario += manager
        scenario += token

        scenario.verify(fractions.data.administrator == addresses.ADMIN)
        scenario += fractions.set_administrator(
            manager.address).run(sender=addresses.ALICE, valid=False)
        scenario += fractions.set_administrator(
            manager.address).run(sender=addresses.ADMIN, valid=True)
        scenario.verify(fractions.data.administrator == manager.address)

        tokenId = 0
        scenario += token.mint(owner=addresses.ALICE,
                               token_id=tokenId, token_amount=1).run(sender=addresses.ADMIN)
        scenario.verify(token.data.ledger[FA2.LedgerKey.make(
            tokenId, addresses.ALICE)] == sp.nat(1))

        scenario += manager.fractionalize(100).run(sender=addresses.ALICE)
        scenario.verify(
            fractions.data.ledger[FA2.LedgerKey.make(0, addresses.ALICE)] == 100)
        scenario.verify(manager.data.next_fractions_token_id == 1)

    # Create vault
    # Fractionalise
    # Redeem
sp.add_compilation_target("manager", Manager(addresses.TOKEN_CONTRACT))
