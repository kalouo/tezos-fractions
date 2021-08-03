import { TezosToolkit } from '@taquito/taquito';
import { InMemorySigner } from '@taquito/signer';

export const configureTezos = async (
  rpcUrl: string,
  privateKeyHash: string
): Promise<TezosToolkit> => {
  const signer = await InMemorySigner.fromSecretKey(privateKeyHash);
  const Tezos = new TezosToolkit(rpcUrl);
  Tezos.setProvider({ signer: signer });

  return Tezos;
};
