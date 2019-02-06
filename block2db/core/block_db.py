from pymongo.errors import DuplicateKeyError

from block2db.core.logger import Logger
from .bitcoin_cli import BitcoinCLI
from .mongo_helper import MongoHelper
from bson.decimal128 import Decimal128


class BlockDB:

    def __init__(self):

        self.cli = BitcoinCLI()
        self.db_collection = 'bitcoin_db'
        self.logger = Logger()

    def iterate_blocks(self, start, end):

        for height in range(start, end):
            self.logger.info("Extracting txns of block height {}".format(height))
            self.iterate_txn(block_height=height)

    def iterate_txn(self, block_height=100000):

        block_hash = self.cli.get_block_hash(block_height)
        block_detail = self.cli.get_block(block_hash)
        txn_list = block_detail['tx']

        mongo_helper = MongoHelper(collection=self.db_collection)

        inserted_ids = []

        for txn in txn_list:
            result = self.get_raw_txn(txn)
            result['block_height'] = block_height
            try:
                inserted_id = mongo_helper.insert(result).inserted_id
                self.logger.info("Inserted txn of id :"+inserted_id)
                inserted_ids.append(inserted_id)
            except DuplicateKeyError:
                self.logger.info("Txn of id {} already exists.".format(txn))

    def get_raw_txn(self, tx_id):
        result = self.cli.get_raw_transaction(tx_id)

        result['_id'] = result.pop('txid', None)
        vins = result.pop('vin', None)
        vouts = result.pop('vout', None)

        inputs = []
        outputs = []

        for each in vins:
            input_dict = {}
            if 'coinbase' in each:
                input_dict['address'] = each['coinbase']
                input_dict['sequence'] = each['sequence']
            else:
                address, value = self.get_prev_out(each['txid'], each['vout'])
                input_dict = dict(address=address, value=Decimal128(str("{0:.8f}".format(value))),
                                  sequence=each['sequence'])

            inputs.append(input_dict)

        for out in vouts:
            output = {'address': out['scriptPubKey']['addresses'][0],
                      'value': Decimal128(str("{0:.8f}".format(out['value']))),
                      'n': out['n']}

            outputs.append(output)

        result['inputs'] = inputs
        result['outputs'] = outputs

        return result

    def get_prev_out(self, tx_id, n):
        result = self.cli.get_raw_transaction(tx_id)
        address = result['vout'][n]['scriptPubKey']['addresses'][0]
        value = result['vout'][n]['value']

        return address, value
