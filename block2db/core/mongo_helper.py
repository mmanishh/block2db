from pymongo import MongoClient

from .constants import Constants


class MongoHelper:

    def __init__(self, collection, username=None, password=None):
        if username is not None and password is not None:
            self.client = MongoClient(Constants.MONGO_DB_URI,
                                      username=username,
                                      password=password)
            self.db = self.client.block2db
            self.collection = collection
        else:
            self.client = MongoClient(Constants.MONGO_DB_URI)
            self.db = self.client.block2db
            self.collection = collection

    def insert(self, dict):
        """
        Insert operation for mongodb
        :param dict: Dictionary value for manual insertion in db
        :return: Boolean as success
        """
        collection = self.db[self.collection]
        return collection.insert_one(dict)

    def insert_or_update(self, filter, update, upsert=True):
        """
        perform an insert if no documents match the filter, if matches the filter updates the document
        :param filter: A query that matches the document to update.
        :param update: The modifications to apply.
        :param upsert : If True, perform an insert if no documents match the filter.
        :return: Boolean as success
        """
        collection = self.db[self.collection]
        collection.update_one(filter, update, upsert=upsert)

        return True

    def find(self, dict=None, projection=None):
        """
        :param dict: Query to find in DB
        :return: Collection of document
        """

        # if dict is None:
        #     data = self.scrap(address)
        # else:
        #     data = dict

        collection = self.db[self.collection]
        return collection.find(dict, projection)
