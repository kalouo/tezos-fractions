import { ContractAbstraction, Wallet } from '@taquito/taquito';
import { useTezosContext } from 'contexts/tezos';
import { useEffect, useState } from 'react';

import { notifyError, notifySuccess } from 'utils/notifier';

export const useManager = () => {
  type Contract = ContractAbstraction<Wallet>;

  const { tezos } = useTezosContext();

  const [loading, setLoading] = useState<boolean>(false);
  const [managerContract, setManagerContract] = useState<Contract>();

  useEffect(() => {
    if (!managerContract) {
      initializeContract('KT1PNohHW9FYMDfkPGMDQvvNuhegoajaQxXR');
    }
  }, [managerContract]);

  async function createVault(assetContractAddress: string, assetTokenId: string) {
    if (!managerContract) {
      notifyError('Error', 'Cannot connect to manager contract.');
      return;
    }

    setLoading(true);
    const storage: { [key: string]: any } = await managerContract.storage();

    const vault = await getVaultByUnderlying(storage, assetContractAddress, assetTokenId);

    if (vault) {
      setLoading(false);
      notifyError('EXISTING VAULT', vault);
    } else {
      try {
        const op = await managerContract.methods
          .create_vault(assetContractAddress, assetTokenId)
          .send();

        await op.confirmation(1);

        setLoading(false);
        notifySuccess('VAULT CREATED', op.opHash);
      } catch (error) {
        setLoading(false);
      }
    }
  }

  async function initializeContract(contractAddress: string) {
    const contract = await tezos?.wallet.at(contractAddress);
    if (contract) {
      setManagerContract(contract);
    } else {
      notifyError('Error', 'Cannot connect to manager contract.');
    }
  }

  async function getVaultByUnderlying(
    storage: { [key: string]: any },
    assetContractAddress: string,
    assetTokenId: string,
  ) {
    return storage.vault_lookup_by_underlying.get({
      contract_address: assetContractAddress,
      token_id: assetTokenId,
    });
  }

  return { loading, createVault };
};
