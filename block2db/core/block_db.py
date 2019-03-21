from bitcoinrpc.authproxy import JSONRPCException
from pymongo.errors import DuplicateKeyError

from block2db.core.logger import Logger
from block2db.core.redis_helper import RedisHelper
from .bitcoin_cli import BitcoinCLI
from .mongo_helper import MongoHelper
from bson.decimal128 import Decimal128


class BlockDB:

    def __init__(self):

        self.cli = BitcoinCLI()
        self.db_collection = 'bitcoin_db'
        self.logger = Logger()
        self.redis = RedisHelper()

    def iterate_blocks(self):
        """
        Iterates block from block height saved in redis to latest block height retrieved from bitcon core
        :return: Boolean success
        """
        start = 1 if self.redis.hget('block_height') is None else \
            int(self.redis.hget('block_height'))  # get block_height checkpoint from redis db
        end = self.cli.get_block_count()

        self.logger.info("block height start:{start} end:{end}".format(start=start, end=end))
        for height in range(start, end):
            self.logger.info("Extracting txns of block height {}".format(height))
            self.iterate_txn(block_height=height)

            # setting block height in redis as checkpoint for future
            self.redis.hset('block_height', height)

        return True

    def iterate_txn(self, block_height):
        """
        Iterates txn list and retrieves detail for each txn
        :param block_height: Block height of the blockchain
        :return: Boolean success
        """
        block_hash = self.cli.get_block_hash(block_height)
        block_detail = self.cli.get_block(block_hash)
        txn_list = block_detail['tx']

        mongo_helper = MongoHelper(collection=self.db_collection)

        inserted_ids = []

        for txn in txn_list:
            try:
                result = self.get_raw_txn(txn)
                result['block_height'] = block_height

                inserted_id = mongo_helper.insert(result).inserted_id
                self.logger.info("Inserted txn of id :" + inserted_id)
                inserted_ids.append(inserted_id)
            except DuplicateKeyError:
                self.logger.info("Txn of id {} already exists.".format(txn))
            except JSONRPCException as e:
                self.logger.info(e.message)

        return True

    def get_raw_txn_deprecated(self, tx_id):
        """
        Gets processed dict of txn details (Not used)
        :param tx_id: Transaction id of bitcoin transaction
        :return: dict of txn detail
        """
        result = self.cli.get_raw_transaction(tx_id)

        try:
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
                    input_dict['type'] = 'coinbase'
                else:
                    address, value = self.get_prev_out(each['txid'], each['vout'])
                    input_dict = dict(address=address, value=Decimal128(str("{0:.8f}".format(value))),
                                      sequence=each['sequence'])

                inputs.append(input_dict)

            for out in vouts:
                if out['scriptPubKey']['type'] == 'nonstandard':
                    output = {'value': Decimal128(str("{0:.8f}".format(out['value']))),
                              'n': out['n']}
                else:
                    output = {'address': out['scriptPubKey']['addresses'][0],
                              'value': Decimal128(str("{0:.8f}".format(out['value']))),
                              'n': out['n']}

                outputs.append(output)

            result['inputs'] = inputs
            result['outputs'] = outputs

        except KeyError as e:
            self.logger.info("Key error for tx: {tx_id}".format(tx_id=tx_id))

        return result

    def get_raw_txn(self, tx_id):
        """
        Gets dict of transaction details of tx_id
        :param tx_id: Transaction id of bitcoin txn
        :return: dict of txn details
        """
        result = self.cli.get_raw_transaction(tx_id)

        try:
            # setting txid as index in document as _id defines index in mongo
            result['_id'] = result.pop('txid', None)

            # popping vout array and converting the value object to Decimal128 object because
            # mongo doesn't support default Decimal object
            vouts = result.pop('vout', None)

            for each in vouts:
                each['value'] = Decimal128(str("{0:.8f}".format(each['value'])))

            result['vout'] = vouts

        except KeyError as e:
            self.logger.info("Key error for tx: {tx_id}".format(tx_id=tx_id))

        return result

    def get_prev_out(self, tx_id, n):
        """
        Get prev output by tx_id and index n
        :param tx_id: Transaction id of bitcoin txn
        :param n: index n
        :return: Tuple address and value
        """
        result = self.cli.get_raw_transaction(tx_id)
        address = result['vout'][n]['scriptPubKey']['addresses'][0]
        value = result['vout'][n]['value']

        return address, value
