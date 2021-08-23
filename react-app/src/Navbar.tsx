import styled from 'styled-components';
import truncateMiddle from 'truncate-middle';
import colors from './utils/colors';
import { useWallet } from './hooks/useWallet';

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
    border: 1px solid ${colors.WHITE};
    padding: 7.5px;
    cursor: pointer;
    :hover {
      background-color: ${colors.GRAY};
    }
  }
`;

const Navbar = () => {
  const {
    initialized, address, connect, disconnect,
  } = useWallet();

  return (
    <Container>
      <div className="inner-container">
        <div className="title">FRAGMENTS</div>
        <div className="provider-button" onClick={() => (initialized ? disconnect() : connect())}>
          {initialized ? `ꜩ ${truncateMiddle(address, 5, 5, ' ... ')}` : 'CONNECT'}
        </div>
      </div>
    </Container>
  );
};

export default Navbar;
