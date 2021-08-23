import { useState } from 'react';
import { useTezosContext } from 'contexts/tezos';
import { NetworkType } from '@airgap/beacon-sdk';
import { notifyError } from 'utils/notifier';

export function useWallet() {
  const { wallet } = useTezosContext();

  const [initialized, setInitialized] = useState(false);
  const [address, setAddress] = useState('');
  const [loading, setLoading] = useState<boolean>(false);

  async function connect() {
    setLoading(true);
    if (wallet) {
      try {
        const response = await wallet.client.requestPermissions({
          network: { type: NetworkType.FLORENCENET },
        });
        setInitialized(true);
        setAddress(response.address);
      } catch (error) {
        notifyError('ERROR', 'Could not connect to wallet.');
      } finally {
        setLoading(false);
      }
    }
  }

  async function disconnect() {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    if (wallet) {
      try {
        await wallet.clearActiveAccount();
        setInitialized(false);
        setAddress('');
      } catch (error) {
        notifyError('ERROR', 'Could not disconnect wallet.');
      }
    }
  }
  return {
    initialized,
    address,
    loading,
    connect,
    disconnect,
  };
}
