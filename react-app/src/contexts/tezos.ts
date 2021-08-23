import { createContext, useContext } from 'react';
import { TezosToolkit } from '@taquito/taquito';
import { BeaconWallet } from '@taquito/beacon-wallet';

interface State {
  tezos?: TezosToolkit;
  wallet?: BeaconWallet;
}

export const TezosContext = createContext<State>({});
export const useTezosContext = (): State => useContext(TezosContext);
