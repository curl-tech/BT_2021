# BT_2021
Bangalore Torpedo 2021 Hackathon Code Repo


## Instructions To Run/Deploy Backend 

### Prerequisite
1. Node Version: v14.17.2
2. Add .env in project root dir
 
### How to Run Backend

To run backend :
1. npm install
2. node app.js

### APIs
1. Upload File:
   POST URL: http://localhost:8080/nature/upload-file
   <pre>
   {
    "artName":"New Art Name",
    "artDescription": "Description of this art",
    "file":"file goes here"
   }
   </pre>
   Unce uploaded, this async API does following perations:
   1. The api calls a python script, gets processed filePath (art output)
   2. Uploads the art and its metadata to IPFS 
   3. The returned ipfs url is used to create a new NFT in Ethereum blockchain ( Rinkeby Testnet) 
   4. Each new NFT created can be tracked in Opensea market here: https://testnets.opensea.io/collection/naturenft-v4
### How To Compile and Deploy Contract
This is not a necessary step, unless you make modification and deploy new contract.
From project root dir do the following things:
1. Install Truffle cli: npm install -g truffle
2. To compile: truffle compile
3. Migration: 

* Deploying to Ganache: truffle migrate
* Deploying to rinkeby_local:
    1. Run a local light Geth node with following command: 
     <pre>geth --rinkeby --syncmode "light" --cache 2048 --rpc --rpcapi db,eth,net,web3,personal --allow-insecure-unlock --unlock="0xddb44367f29ba53489d527247b991f32cda5526f"</pre>
    3. To deploy run: truffle console --network rinkeby_local

* Deploying to rinkeby_infura:
    1. To deploy to rinkeby using infura place .env in root project
    2. To deploy run: truffle migrate --network rinkeby_infura --reset --compile-all




