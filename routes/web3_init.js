const HDWalletProvider = require("@truffle/hdwallet-provider");
const Web3 = require("web3");
const MNEMONIC = process.env.MNEMONIC ;
const INFURA_URL = process.env.INFURA_URL ;

let provider = new HDWalletProvider({
  mnemonic: {
    phrase: MNEMONIC
  },
  providerOrUrl: INFURA_URL
});

const web3 = new Web3(provider);

module.exports = web3 ; 