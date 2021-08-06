import smartpy as sp

import contracts.FA2 as FA2 

Addresses = {
    "ADMIN": sp.address("tz1VQnqCCqX4K5sP3FNkVSNKTdCAMJDd3E1n"),
    "ALICE": sp.address("tz1MJx9vhaNRSimcuXPK2rW4fLccQnDAnVKJ"),
    "BOB": sp.address("tz1eEnQhbwf6trb8Q8mPb2RaPkNk2rN7BKi8"),
    "TOKEN_CONTRACT": sp.address("KT1HbQepzV1nVGg8QVznG7z4RcHseD5kwqBn")
}


class Utils:
    """Utils class to facilitate certain operation. This is just syntactic sugar.
    """
    def execute_token_transfer(token_address, from_, to_, token_id, amount):
        """executes a single fa2 token transfer
        Args:
            token_address (sp.address): token address
            from_ (sp.address): sender
            to_ (sp.address): recipient
            token_id (sp.nat): token id
            amount (sp.nat): token amount to transfer
        """
        transfer_token_contract = sp.contract(FA2.Transfer.get_batch_type(
            ), token_address, entry_point="transfer").open_some()
        transfer_payload = [FA2.Transfer.item(from_, [sp.record(
                to_=to_, token_id=token_id, amount=amount)])]
        sp.transfer(transfer_payload, sp.mutez(0), transfer_token_contract)
