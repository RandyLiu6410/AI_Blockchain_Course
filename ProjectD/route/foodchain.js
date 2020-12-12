const router = require('express').Router();

const Web3 = require('web3');
const quorumjs = require('quorum-js');
const web3 = new Web3(process.env.NODE1);
quorumjs.extend(web3);

var abi = require('../food3.json');
const contract = new web3.eth.Contract(abi, '0xA4fafbE0ea4823e262b4916EF93CC5A6306A5DBc');

router.route('/').get((req, res) => {
    contract.getPastEvents("allEvents",
        {                               
            fromBlock: req.query.START_BLOCK,     
            toBlock: 'latest'        
        })                              
    .then(events => {
        const result = events.find(e => e.returnValues['logno'] === req.query.logno);
        if(result){
            res.json(result);
        }else {
            res.json('no result');
        }
    })
    .catch((err) => console.error(err));
});

module.exports = router;