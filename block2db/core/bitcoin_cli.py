from bitcoinrpc.authproxy import AuthServiceProxy


class BitcoinCLI:

    def __init__(self, rpc_user=None, rpc_pass=None):
        # rpc_user and rpc_password are set in the bitcoin.conf file
        if rpc_user is None and rpc_pass is None:
            rpc_user = 'manish'
            rpc_pass = '8ak1gI25KFTvjovL3gAM967mies3E='
        #self.rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332" % (rpc_user, rpc_pass),timeout=180)
        self.rpc_connection = AuthServiceProxy(
            "http://%s:%s@5.196.65.205:8332" % ("bitcoinrpc", "JRkDy3tgCYdmCEqY1VdfdfhTswiRva"),timeout=600)

    def get_best_block_hash(self):
        return self.rpc_connection.getbestblockhash()

    def get_block_count(self):
        return self.rpc_connection.getblockcount()

    def get_best_block(self):
        return self.rpc_connection.getblock(self.rpc_connection.getbestblockhash())

    def get_block_hash(self, height):
        return self.rpc_connection.getblockhash(height)

    def get_block(self, hash):
        return self.rpc_connection.getblock(hash)

    def get_txn_list_from_block(self, hash):
        block = self.get_block(hash)

        if 'tx' in block:
            return block['tx']
        else:
            raise KeyError('Block {0} has no attribute tx'.format(hash))

    def get_raw_transaction(self, tx_id):
        out = self.rpc_connection.getrawtransaction(tx_id, 1)
        return out

    def get_tx_outputs(self, tx_id):
        tx = self.rpc_connection.getrawtransaction(tx_id, 1)
        outputs = [float(i['value']) for i in tx['vout']]
        return outputs

    def get_tx_details(self, tx_id):
        tx = self.rpc_connection.getrawtransaction(tx_id, 1)
        outputs = [float(i['value']) for i in tx['vout']]
        return outputs
