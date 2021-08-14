import { useState } from "react";
import { TezosToolkit } from "@taquito/taquito";
import { BeaconWallet } from "@taquito/beacon-wallet";

export function useWallet() {
  const [initialized, setInitialized] = useState(false);
  const [address, setAddress] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState<boolean>(false);

  return { initialized, address, error, loading, connect, disconnect };

  async function connect() {
    setLoading(true);

    try {
      const Tezos = new TezosToolkit("https://florencenet.smartpy.io");
      const wallet = new BeaconWallet({ name: "Fragments" });

      Tezos.setWalletProvider(wallet);
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const { address } = await wallet.client.requestPermissions();
      setInitialized(true);
      setAddress(address);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }

  async function disconnect() {
    const Tezos = new TezosToolkit("https://florencenet.smartpy.io");
    const wallet = new BeaconWallet({ name: "Fragments" });

    Tezos.setWalletProvider(wallet);

    await new Promise((resolve) => setTimeout(resolve, 1000));

    try {
      await wallet.clearActiveAccount();
      setInitialized(false);
      setAddress("");
    } catch (error) {
      setError(error.message);
    }
  }
}
