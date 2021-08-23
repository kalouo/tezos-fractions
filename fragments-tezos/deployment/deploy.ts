/* eslint-disable @typescript-eslint/no-var-requires */
import * as dotenv from 'dotenv';
import { configureTezos } from './provider';

const Manager = require('../build/manager.json');

dotenv.config();

const deploy = async () => {
  const { TEZOS_RPC_URL, ORIGINATOR_PRIVATE_KEY } = process.env;
  const Tezos = await configureTezos(TEZOS_RPC_URL, ORIGINATOR_PRIVATE_KEY);

  try {
    const { hash, contractAddress } = await Tezos.contract.originate({
      code: Manager,
      init: require("../build/manager_storage.json")
    });

    console.log('Originated contract');
    console.log(`>> Transaction hash: ${hash}`);
    console.log(`>> Contract address: ${contractAddress}`);
  } catch (error) {
    console.log(error);
  }
};

deploy();
