import React, { useState } from 'react';
import styled from 'styled-components';
import { TextField, Button } from '@material-ui/core';

import Loader from 'components/Loader';

import { useManager } from 'hooks/useManager';
import { isValidContractAddress, isValidTokenId } from 'utils/validators';
import colors from 'utils/colors';

const Container = styled.div`
  border: 1px solid ${colors.BLACK};
  height: 300px;
  margin: 5% 30% 30% 30%;
  display: flex;
  padding: 20px;
  flex-direction: column;
  justify-content: space-between;
  .title {
    text-align: center;
  }
  .fields {
    height: 50%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
`;

function TokenInfo() {
  const { createVault, loading } = useManager();

  const [contractAddress, setContractAddress] = useState<string>('');
  const [tokenId, setTokenId] = useState<string>('');

  const [validCtrAddress, setValidCtrAddress] = useState<boolean>(true);
  const [validTokenId, setValidTokenId] = useState<boolean>(true);

  const handleChange = (
    callback: React.Dispatch<React.SetStateAction<string>>,
  ): React.ChangeEventHandler<HTMLInputElement> => (e) => {
    setValidCtrAddress(true);
    setValidTokenId(true);
    callback(e.target.value);
  };

  const submit: React.MouseEventHandler<HTMLButtonElement> = () => {
    if (!isValidContractAddress(contractAddress)) {
      setValidCtrAddress(false);
      return;
    }

    if (!isValidTokenId(tokenId)) {
      setValidTokenId(false);
      return;
    }

    createVault(contractAddress, tokenId);
  };

  return (
    <Container>
      <div className="title"> CREATE A VAULT </div>
      <div className="fields">
        <TextField
          label="Contract address"
          variant="outlined"
          onChange={handleChange(setContractAddress)}
          error={!validCtrAddress}
          helperText={validCtrAddress ? '' : 'Invalid contract address'}
        />

        <TextField
          label="Token ID"
          variant="outlined"
          onChange={handleChange(setTokenId)}
          error={!validTokenId}
          helperText={validTokenId ? '' : 'Must be an integer.'}
        />
      </div>
      <Button variant="contained" disableElevation onClick={submit}>
        CREATE
      </Button>
      <Loader loading={loading} />
    </Container>
  );
}

export default TokenInfo;
