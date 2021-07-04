var express = require('express');
var router = express.Router();
const PINATA_API_KEY = process.env.PINATA_API_KEY;
const PINATA_API_SECRET = process.env.PINATA_API_SECRET;
const pinataSDK = require('@pinata/sdk');
const { Readable } = require('stream');
const fs = require('fs');
const web3 = require("./web3_init");
const NatureNFT = require("../compiled_contracts/NatureNFT.json");
const MongoService = require("./mongo");
const { spawn } = require('child_process');
const { resolve } = require('path');
const pinata = pinataSDK(PINATA_API_KEY, PINATA_API_SECRET);



router.get('/accounts', async function (req, res, next) {
  const accounts = await web3.eth.getAccounts();
  res.send(accounts);
});


router.get('/sattvas', function (req, res, next) {
  MongoService.getArtCollection().then(result=>res.send(result));
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
  generateArt(req.files.file).then(processedData => {
    uploadFilesToIpfs(req.files.file, processedData, artName, artDescription).then(result => {
      createNFT(result, artName, artDescription);
    }).catch(err => {
      console.log(err);
    });
  }).catch(err => {
    console.log(err);
  });

  res.status(200).send();
});

function checkIpfsConnection() {
  return pinata.testAuthentication();
}

function generateArt(file) {
  return new Promise((resolve, reject) => {
    const python = spawn('python', ['./python/script.py', file.tempFilePath, file.name]);
    python.stdout.on('data', function (data) {
      console.log('Pipe data from python script ...');
      let processedFilePath = data.toString();
      processedFilePath = processedFilePath.replace(/(\r\n|\n|\r)/gm, "");
      console.log("Received Processed FilePath from Python:" + processedFilePath);
      resolve({ "filePath": processedFilePath, "fileName": file.name });
    });
  })
}

function uploadFilesToIpfs(originalFile, processedData, artName, artDescription) {

  return new Promise((resolve, reject) => {
    let artStream = fs.createReadStream(processedData.filePath);
    let artOptions = {
      pinataMetadata: {
        name: originalFile.name,
      }
    };
    const pinOriginalPromise = pinOriginal(artStream, artOptions);
    const pinArtPromise = pinART(artStream, artOptions, artName, artDescription);

    Promise.all([pinOriginalPromise, pinArtPromise]).then(results => {
      let originalResult = results[0];
      let artResult = results[1];
      resolve({ "originalIpfsHash": originalResult.IpfsHash, "artIpfsHash": artResult.artIpfsHash, "metadataIpfsHash": artResult.metadataIpfsHash });
    }).catch(error => {
      console.error(error.message)
    });
  });

}

function pinOriginal(stream, options) {
  return new Promise((resolve, reject) => {
    pinata.pinFileToIPFS(stream, options).then((result) => {
      resolve(result);
    });
  });
}


function pinART(stream, options, artName, artDescription) {
  return new Promise((resolve, reject) => {
    pinata.pinFileToIPFS(stream, options).then((result) => {
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
        resolve({ "artIpfsHash": result.IpfsHash, "metadataIpfsHash": metadataResult.IpfsHash });
      }).catch(err => {
        reject(err);
      })
    }).catch((err) => {
      reject(err);
    });
  })
}

async function createNFT(ipfsFileHashes, artName, artDescription) {
  const accounts = await web3.eth.getAccounts();
  const networkId = await web3.eth.net.getId();
  const deployedNetwork = NatureNFT.networks[networkId];
  const contractInstance = new web3.eth.Contract(
    NatureNFT.abi,
    deployedNetwork && deployedNetwork.address,
  );
  let res = await contractInstance.methods.createArt(accounts[0], "ipfs://" + ipfsFileHashes.metadataIpfsHash).send({ from: accounts[0] });
  console.log("Created NFT, TXN: " + res.transactionHash);
  let dataToSave = {
    artName: artName,
    artDescription: artDescription,
    originalFileURL: "https://gateway.pinata.cloud/ipfs/" + ipfsFileHashes.originalIpfsHash,
    artFileURL: "https://gateway.pinata.cloud/ipfs/" + ipfsFileHashes.artIpfsHash,
  }
  MongoService.saveArtDetails(dataToSave);
}


module.exports = router;
