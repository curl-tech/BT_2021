var NatureNFT = artifacts.require("./contracts/NatureNFT.sol");

module.exports = function(deployer) {
  deployer.deploy(NatureNFT);
};
