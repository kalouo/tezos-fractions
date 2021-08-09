/* eslint-disable @typescript-eslint/no-var-requires */
import * as dotenv from 'dotenv';
import { configureTezos } from './provider';

dotenv.config();

const deploy = async () => {
  const { TEZOS_RPC_URL, ORIGINATOR_PRIVATE_KEY } = process.env;
  const Tezos = await configureTezos(TEZOS_RPC_URL, ORIGINATOR_PRIVATE_KEY);

  const { hash, contractAddress } = await Tezos.contract.originate({
    code: require('./demo.json'),
    storage: { x: 1, y: 2 },
  });

  console.log('Originated contract');
  console.log(`>> Transaction hash: ${hash}`);
  console.log(`>> Contract address: ${contractAddress}`);
};

deploy();
