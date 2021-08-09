import smartpy as sp

import contracts.FA2 as FA2


class Utils:
    """Class to facilitate FA2 operations.
    """
    def execute_token_transfer(token_address, from_, to_, token_id, amount):
        """Executes FA2 token transfer
        Args:
            token_address (sp.address): FA2 token contract address
            from_ (sp.address): sender
            to_ (sp.address): recipient
            token_id (sp.nat): token ID
            amount (sp.nat): token amount to transfer
        """
        transfer_token_contract = sp.contract(FA2.Transfer.get_batch_type(
        ), token_address, entry_point="transfer").open_some()
        transfer_payload = [FA2.Transfer.item(from_, [sp.record(
            to_=to_, token_id=token_id, amount=amount)])]
        sp.transfer(transfer_payload, sp.mutez(0), transfer_token_contract)

    def execute_token_mint(token_address, to_, token_id, amount):
        """Executes FA2 mint transaction
        Args:
            token_address (sp.address): FA2 token contract address
            to_ (sp.address): recipient
            token_id (sp.nat): token ID
            amount (sp.nat): token amount to mint
        """
        mint_token_contract = sp.contract(FA2.RecipientTokenAmount.get_type(
        ), token_address, entry_point='mint').open_some()
        mint_payload = FA2.RecipientTokenAmount.make(to_, token_id, amount)
        sp.transfer(mint_payload, sp.mutez(0), mint_token_contract)


    def execute_token_burn(token_address, from_, token_id, amount):
        """Executes FA2 burn transaction
        Args:
            token_address (sp.address): FA2 token contract address
            to_ (sp.address): recipient
            token_id (sp.nat): token ID
            amount (sp.nat): token amount to mint
        """
        token_contract = sp.contract(FA2.RecipientTokenAmount.get_type(
        ), token_address, entry_point='burn').open_some()
        payload = FA2.RecipientTokenAmount.make(from_, token_id, amount)
        sp.transfer(payload, sp.mutez(0), token_contract)