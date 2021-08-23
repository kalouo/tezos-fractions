import { validateContractAddress, ValidationResult } from '@taquito/utils';

export const isValidContractAddress = (address: string) => validateContractAddress(address) === ValidationResult.VALID;

export const isValidTokenId = (input: string) => Number.isInteger(Number(input));
