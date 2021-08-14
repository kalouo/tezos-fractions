import { useEffect } from "react";
import styled from "styled-components";
import colors from "./colors";
import { TezosToolkit } from "@taquito/taquito";
import { BeaconWallet } from "@taquito/beacon-wallet";
import { useWallet } from "./hooks/useWallet";
import truncateMiddle from "truncate-middle";

const Container = styled.div`
  background-color: ${colors.BLACK};
  height: 10vh;
  padding: 0 2%;
  .inner-container {
    height: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  .title {
    color: ${colors.WHITE};
    font-size: 48px;
  }
  .provider-button {
    color: ${colors.WHITE};
    border-color: ${colors.WHITE};
    border: 1px solid ${colors.WHITE};
    padding: 7.5px;
    cursor: pointer;
    :hover {
      background-color: ${colors.GRAY};
    }
  }
`;

const Navbar = () => {
  // const {
  //   initialized,
  //   address,
  //   error: walletError,
  //   loading: walletLoading,
  //   connect: connect,
  // } = useBeaconWallet();

  const { initialized, address, error, connect, disconnect } = useWallet();

  return (
    <Container>
      <div className="inner-container">
        <div className="title">FRAGMENTS</div>
        <div
          className="provider-button"
          onClick={() => (initialized ? disconnect() : connect())}
        >
          {initialized ? `ꜩ ${truncateMiddle(address, 5, 5, " ... ")}` : "CONNECT"}
        </div>
      </div>
    </Container>
  );
};

export default Navbar;
