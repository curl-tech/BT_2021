var express = require('express');
var router = express.Router();
const pinataSDK = require('@pinata/sdk');
const pinata = pinataSDK('ce337d9a240c058c587c', '9b17607f378b1316894dad757278d4481e96ebdf826b846f85f988de65e5ed98');
const { Readable } = require('stream');
const fs = require('fs');
const web3 = require("./web3_init");
const NatureNFT = require("../compiled_contracts/NatureNFT.json");
const {spawn} = require('child_process');

router.get('/accounts', async function (req, res, next) {
  const accounts = await web3.eth.getAccounts();
  res.send(accounts);
});


router.post('/upload-file', async function (req, res) {

  if (!req.files || Object.keys(req.files).length === 0) {
    res.status(400).send({ "message": 'No file uploaded' });
    return;
  }
  if (req.files.length > 1)
    res.status(400).send({ "message": 'Multiple files upload not supported yet' });
  else if (!req.files.file)
    res.status(400).send({ "message": 'File key should be file' });

  let artDescription = req.body.artDescription ? req.body.artDescription : "";
  let artName = req.body.artName ? req.body.artName : "";
  let connection = await checkIpfsConnection();
  if (!connection.authenticated)
    res.status(400).send({ "message": "Cannot reach ipfs server" });

  generateArt(req.files.file).then(processedData=>{
    uploadFileToIpfs(processedData, artName, artDescription).then(result => {
      createNFT(result.IpfsHash);
    }).catch(err => {
      console.log(err);
    });
  }).catch(err=>{
    console.log(err);
  });

  res.status(200).send();
});

function checkIpfsConnection() {
  return pinata.testAuthentication();
}

function generateArt(file){
  return new Promise((resolve,reject)=>{
    const python = spawn('python', ['./python/script.py',file.tempFilePath,file.name]);
    python.stdout.on('data', function (data) {
      console.log('Pipe data from python script ...');      
      let processedFilePath = data.toString();
      processedFilePath = processedFilePath.replace(/(\r\n|\n|\r)/gm, "");
      console.log("Received Processed FilePath from Python:"+processedFilePath);
      resolve({"filePath":processedFilePath,"fileName":file.name});
    });    
  })
}

function uploadFileToIpfs(processedData, artName, artDescription) {

  return new Promise((resolve, reject) => {
    let validStream = fs.createReadStream(processedData.filePath);
    let options = {
      pinataMetadata: {
        name: processedData.fileName,
      }
    };
    pinata.pinFileToIPFS(validStream, options).then((result) => {
      let metadataOptions = {
        pinataMetadata: {
          name: result.IpfsHash + "_metadata",
        }
      };
      let metadata = {
        name: artName,
        description: artDescription,
        image: "https://gateway.pinata.cloud/ipfs/" + result.IpfsHash
      }

      pinata.pinJSONToIPFS(metadata, metadataOptions).then(metadataResult => {
        resolve(metadataResult);
      }).catch(err => {
        reject(err);
      })
    }).catch((err) => {
      reject(err);
    });


  });

}

async function createNFT(ipfsHash) {
  const accounts = await web3.eth.getAccounts();
  const networkId = await web3.eth.net.getId();
  const deployedNetwork = NatureNFT.networks[networkId];
  const contractInstance = new web3.eth.Contract(
    NatureNFT.abi,
    deployedNetwork && deployedNetwork.address,
  );
  let res = await contractInstance.methods.createArt(accounts[0], "ipfs://" + ipfsHash).send({ from: accounts[0] });
  console.log("Created NFT, TXN: " + res.transactionHash);
}


module.exports = router;
