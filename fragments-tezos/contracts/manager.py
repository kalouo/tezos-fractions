import smartpy as sp

from contracts.vault import Vault
from contracts.viewer import Viewer
from contracts.utils import Utils

import contracts.FA2 as FA2


class ErrorMessage:
    EXISTING_VAULT = "{}EXISTING_VAULT"
    """This error is thrown if the token already has a corresponding vault"""
    NO_VAULT_FOUND = "{}NO_VAULT_FOUND"
    """This error is thrown if a fractionalisation is requested without a a pre-existing vault."""
    INVALID_FRACTIONS_AMOUNT = "{}INVALID_FRACTIONS_AMOUNT"
    """This error is thrown if the user requests to emit less than one fraction"""
    ALREADY_FRACTIONALIZED = "{}ALREADY_FRACTIONALIZED"
    """This error is thrown if fractions are already outstanding for the given token"""


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
        self.init(**self.get_initial_storage(fractions_contract))

    @sp.entry_point
    def create_vault(self, asset_contract, asset_token_id):
        sp.set_type(asset_contract, sp.TAddress)
        sp.set_type(asset_token_id, sp.TNat)

        lookup_key = LookupKey.make(asset_contract, asset_token_id)
        sp.verify(self.data.vault_lookup_by_underlying.contains(
            lookup_key) == False, message=ErrorMessage.EXISTING_VAULT)

        vault_contract_address = sp.create_contract(Vault(sp.self_address))

        self.data.vault_lookup_by_underlying[lookup_key] = vault_contract_address


    @sp.entry_point
    def deposit_and_fractionalise(self, asset_contract_address, asset_token_id, supply):
        sp.set_type(asset_contract_address, sp.TAddress)
        sp.set_type(asset_token_id, sp.TNat)
        sp.set_type(supply, sp.TNat)

        sp.verify(supply > 0, message=ErrorMessage.INVALID_FRACTIONS_AMOUNT)

        vault_address = self.get_vault(asset_contract_address, asset_token_id)
        sp.verify(self.data.vaults.contains(vault_address) == False,
                  message=ErrorMessage.ALREADY_FRACTIONALIZED)

        Utils.execute_token_transfer(
            asset_contract_address,
            sp.sender,
            vault_address,
            asset_token_id,
            sp.nat(1)
        )

        Utils.execute_token_mint(
            self.data.fractions_contract,
            sp.sender,
            self.data.next_fractions_token_id,
            supply
        )

        self.data.vault_lookup_by_fractions_token_id[
            self.data.next_fractions_token_id] = vault_address

        self.data.vaults[vault_address] = sp.record(
            minted=supply, fractions_token_id=self.data.next_fractions_token_id)

        self.data.next_fractions_token_id += 1

    @sp.entry_point
    def redeem(self, asset_contract_address, asset_token_id):
        sp.set_type(asset_contract_address, sp.TAddress)
        sp.set_type(asset_token_id, sp.TNat)

        vault = self.get_vault(asset_contract_address, asset_token_id)
        fractions_id = self.data.vaults[vault].fractions_token_id
        outstanding_fractions = self.data.vaults[vault].minted

        Utils.execute_token_burn(
            self.data.fractions_contract, sp.sender, fractions_id, outstanding_fractions)

        vault_contract = sp.contract(sp.TRecord(asset_contract_address=sp.TAddress, asset_token_id=sp.TNat, recipient=sp.TAddress), vault, entry_point='send_asset').open_some()
        payload = sp.record(asset_contract_address=asset_contract_address,
                            asset_token_id=asset_token_id, recipient=sp.sender)
        sp.transfer(payload, sp.mutez(0), vault_contract)

    
    
    
    def get_fractions_id_by_underlying(self, asset_contract_address, asset_token_id):
        vault = self.get_vault(asset_contract_address, asset_token_id)
        return self.data.vaults[vault]["fractions_token_id"]

    def get_vault(self, asset_contract_address, asset_token_id):
        lookup_key = LookupKey.make(asset_contract_address, asset_token_id)
        sp.verify(self.data.vault_lookup_by_underlying.contains(
            lookup_key), message=ErrorMessage.NO_VAULT_FOUND)

        return self.data.vault_lookup_by_underlying[lookup_key]

    def get_initial_storage(self, fractions_contract):
        storage = {}
        storage['next_fractions_token_id'] = 0
        storage['fractions_contract'] = fractions_contract

        vault_context_type = sp.TRecord(
            minted=sp.TNat, fractions_token_id=sp.TNat)
        storage['vaults'] = sp.big_map(
            tkey=sp.TAddress, tvalue=vault_context_type)
        storage['vault_lookup_by_fractions_token_id'] = sp.big_map(
            tkey=sp.TNat, tvalue=sp.TAddress)
        storage['vault_lookup_by_underlying'] = sp.big_map(
            tkey=LookupKey.get_type(), tvalue=sp.TAddress)

        return storage

    @sp.add_test(name="Manager")
    def test():
        scenario = sp.test_scenario()

        # Initialisation

        admin = sp.test_account("Administrator")
        alice = sp.test_account("Alice")

        fractions = FA2.AdministrableFA2(admin.address)
        manager = Manager(fractions_contract=fractions.address)
        token = FA2.AdministrableFA2(admin.address)
        viewer = Viewer()

        scenario += fractions
        scenario += manager
        scenario += token
        scenario += viewer

        scenario.verify(fractions.data.administrator == admin.address)
        scenario += fractions.set_administrator(
            manager.address).run(sender=alice.address, valid=False)
        scenario += fractions.set_administrator(
            manager.address).run(sender=admin.address, valid=True)
        scenario.verify(fractions.data.administrator == manager.address)

        token_id = 0
        scenario += token.mint(owner=alice.address,
                               token_id=token_id, token_amount=1).run(sender=admin.address)
        scenario.verify(token.data.ledger[FA2.LedgerKey.make(
            token_id, alice.address)] == sp.nat(1))

        return_contract = sp.contract(
            sp.TAddress, viewer.address).open_some()

        scenario += manager.deposit_and_fractionalise(asset_contract_address=token.address,
                                                      asset_token_id=token_id, supply=100).run(sender=alice.address, valid=False, exception=ErrorMessage.NO_VAULT_FOUND)

        scenario += manager.create_vault(asset_contract=token.address,
                                         asset_token_id=0,
                                         contract_address_callback=return_contract).run(sender=alice.address)

        scenario += manager.create_vault(asset_contract=token.address,
                                         asset_token_id=0,
                                         contract_address_callback=return_contract).run(sender=alice.address, valid=False, exception=ErrorMessage.EXISTING_VAULT)

        lookup_key = LookupKey.make(token.address, token_id)
        vault_address =  manager.data.vault_lookup_by_underlying[lookup_key]

        # Alice deposits in the Vault.
        scenario += token.update_operators([sp.variant("add_operator", sp.record(
            owner=alice.address,
            operator=manager.address,
            token_id=token_id
        ))]).run(sender=alice.address)

        scenario += manager.deposit_and_fractionalise(
            asset_contract_address=token.address, asset_token_id=token_id, supply=0).run(sender=alice.address, valid=False, exception=ErrorMessage.INVALID_FRACTIONS_AMOUNT)

        scenario += manager.deposit_and_fractionalise(
            asset_contract_address=token.address, asset_token_id=token_id, supply=100).run(sender=alice.address)

        scenario += manager.deposit_and_fractionalise(
            asset_contract_address=token.address, asset_token_id=token_id, supply=100).run(sender=alice.address, valid=False, exception=ErrorMessage.ALREADY_FRACTIONALIZED)

        scenario.verify(token.data.ledger[FA2.LedgerKey.make(
            token_id, vault_address)] == sp.nat(1))

        scenario.verify(token.data.ledger.contains(
            FA2.LedgerKey.make(token_id, alice.address)) == False)

        scenario.verify(
            fractions.data.ledger[FA2.LedgerKey.make(0, alice.address)] == 100)
        scenario.verify(manager.data.next_fractions_token_id == 1)
        scenario.verify(manager.data.vaults[vault_address] == sp.record(
            minted=100, fractions_token_id=0))
        scenario.verify(
            manager.data.vault_lookup_by_fractions_token_id[0] == vault_address)

        scenario += manager.redeem(asset_contract_address=token.address, asset_token_id=token_id).run(sender = alice.address)
        scenario.verify(token.data.ledger[FA2.LedgerKey.make(token_id, alice.address)] == sp.nat(1))
        scenario.verify(fractions.data.ledger.contains(FA2.LedgerKey.make(0, alice.address)) == False)

sp.add_compilation_target("manager", Manager(
    sp.address("tz1eeR22tmjPN3rGDikEMvpe8jcdXww3dqTt")))
