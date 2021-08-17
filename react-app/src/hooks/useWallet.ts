import { useState } from "react";
import { useTezosContext } from "context/tezos";

export function useWallet() {
  const { wallet } = useTezosContext();

  const [initialized, setInitialized] = useState(false);
  const [address, setAddress] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState<boolean>(false);

  return { initialized, address, error, loading, connect, disconnect };

  async function connect() {
    setLoading(true);
    if (wallet) {
      try {
        const { address } = await wallet.client.requestPermissions();
        setInitialized(true);
        setAddress(address);
      } catch (error) {
        setError(error.message);
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
        setAddress("");
      } catch (error) {
        setError(error.message);
      }
    }
  }
}
