import { TezosContext } from 'contexts/tezos';
import { TezosToolkit } from '@taquito/taquito';
import { BeaconWallet } from '@taquito/beacon-wallet';
import { NetworkType } from '@airgap/beacon-sdk';
import ReactNotification from 'react-notifications-component';
import 'react-notifications-component/dist/theme.css';
import Router from './Router';

export default function App() {
  const tezos = new TezosToolkit('https://florencenet.smartpy.io');
  const wallet = new BeaconWallet({
    name: 'Fragments',
    preferredNetwork: NetworkType.FLORENCENET,
  });

  tezos.setWalletProvider(wallet);

  return (
    <TezosContext.Provider value={{ tezos, wallet }}>
      <ReactNotification />
      <Router />
    </TezosContext.Provider>
  );
}
