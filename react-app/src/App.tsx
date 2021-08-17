import MasterForm from "./MasterForm";
import Navbar from "./Navbar";

import { TezosContext } from "context/tezos";
import { TezosToolkit } from "@taquito/taquito";
import { BeaconWallet } from "@taquito/beacon-wallet";

export default function App() {
  const tezos = new TezosToolkit("https://florencenet.smartpy.io");
  const wallet = new BeaconWallet({ name: "Fragments" });

  tezos.setWalletProvider(wallet);

  return (
    <TezosContext.Provider value={{ tezos, wallet }}>
      <Navbar></Navbar>
      <MasterForm></MasterForm>
    </TezosContext.Provider>
  );
}
