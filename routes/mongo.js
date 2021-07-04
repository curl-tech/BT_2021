var MongoClient = require('mongodb').MongoClient
var sattvaDb = null;
MongoClient.connect('mongodb://localhost:27017/sattva', function (err, client) {
    if (err) throw err
    sattvaDb = client.db('sattva')
})

function saveArtDetails(doc) {
    let collection = sattvaDb.collection('art');
    const result = collection.insertOne(doc);
    console.log(
        `Documents were inserted successfully`,
    );
}

function getArtCollection() {
    return new Promise((resolve) => {
        sattvaDb.collection('art').find().toArray(function (err, result) {
            if (err) throw err
            resolve(result);
        });
    })
}
module.exports = {
    saveArtDetails: saveArtDetails,
    getArtCollection: getArtCollection
};