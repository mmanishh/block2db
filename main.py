from block2db.core.bitcoin_cli import BitcoinCLI
import json

from block2db.core.block_db import BlockDB


def main():
    bitcoin_cli = BitcoinCLI()

    # print('best block:', bitcoin_cli.get_best_block())
    # print('best block hash:', bitcoin_cli.get_best_block_hash())
    # print('block hash:', bitcoin_cli.get_block_hash(1))
    # print('block:', bitcoin_cli.get_block(bitcoin_cli.get_block_hash(1)))
    # print('raw transaction:',bitcoin_cli.get_raw_transaction('63522845d294ee9b0188ae5cac91bf389a0c3723f084ca1025e7d9cdfe481ce1'))
    # print('outputs:', bitcoin_cli.get_tx_outputs('63522845d294ee9b0188ae5cac91bf389a0c3723f084ca1025e7d9cdfe481ce1'))
    #
    # print('txn list:', bitcoin_cli.get_txn_list_from_block(bitcoin_cli.get_block_hash(1000)))

    print('block count:', bitcoin_cli.get_block_count())

    block_db = BlockDB()

    result = block_db.get_raw_txn('5481ccb8fd867ae90ae33793fff2b6bcd93f8881f1c883035f955c59d4fa8322')

    #print(json.dumps(result, indent=4))
    # 'fff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4'

    block_db.iterate_blocks(100000,100050)




if __name__ == "__main__":
    main()
