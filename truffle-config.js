const path = require("path");
require('dotenv').config();
var HDWalletProvider = require("truffle-hdwallet-provider");
const INFURA_URL = process.env.INFURA_URL ;
const MNEMONIC = process.env.MNEMONIC ;
const RINKEBY_LOCAL_ADDRESS = process.env.RINKEBY_LOCAL_ADDRESS ;
module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
  contracts_build_directory: path.join(__dirname, "compiled_contracts"),
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545,
      network_id: "*" // Match any network id
    },
    rinkeby_local: {
      host: "localhost", // Connect to geth on the specified
      port: 8545,
      from: RINKEBY_LOCAL_ADDRESS, // default address to use for any transaction Truffle makes during migrations, here accounts needs to be unlocked
      network_id: 4,
      gas: 4612388
    },
    rinkeby_infura: {
      provider: function () {
        return new HDWalletProvider(MNEMONIC, INFURA_URL);
      },
      network_id: 4,
      gas: 4500000,
      gasPrice: 10000000000,
    }
  },
  compilers: {
    solc: {
      version: "^0.8.0"
    }
  }
};
