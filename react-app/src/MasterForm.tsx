import { useState } from 'react';
import TokenInfo from './TokenInfo';

const MasterForm = () => {
  const [step, setStep] = useState<number>(1);

  const [assetContract, setAssetContract] = useState<string>('');
  const [assetId, setAssetId] = useState<string>('');

  switch (step) {
    case 1:
      return <TokenInfo />;
    case 2:
      return <div />;
    case 3:
      return <div />;
    case 4:
      return <div />;
    default:
      return <div />;
  }
};

export default MasterForm;
