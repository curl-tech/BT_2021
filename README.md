# BT_2021
Bangalore Torpedo 2021 Hackathon Code Repo


## Instructions To Run Backend and Deploy Backend

### How to Run Backend

To run backend :
1. npm install
2. node app.js


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




