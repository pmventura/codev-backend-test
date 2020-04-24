from flask_restplus import Resource, reqparse
from elasticsearch import Elasticsearch
parser = reqparse.RequestParser()
import os.path
from os import path
from datetime import datetime
from config import Config
es = Elasticsearch(Config.ELASTICSEARCH_URL)
from pathlib import Path


class User(Resource):

    def get(self):
        """
        Return all ES documents
        :return:
        """
        res = es.search(index="users", doc_type="document_id")
        data = [data['_source'] for data in res['hits']['hits']]
        return {
            "fs_metadata": data,
            "message": "Success",
            "status_code": 200
        }

    def post(self):
        """
        This method will handle creation of fs
        :return:
        """
        try:
            parser.add_argument("file_path", type=str, required=True)
            args = parser.parse_args()

            body = {
                "file_path": args["file_path"]
            }

            ROOT_DIR = os.path.dirname(os.path.realpath(__file__)).rsplit(os.sep, 2)[0]
            file_path = os.path.join(ROOT_DIR, body["file_path"])

            if not path.exists(file_path):
                raise Exception("Path doesn't exist")

            if path.isfile(file_path):
                body["extension"] = os.path.splitext(body["file_path"])[1]

            today = datetime.timestamp(datetime.now())
            body["date_ingested"] = today
            es.index(index=f"fs_metadata_{today}", doc_type="file", id=body["file_path"], body=body)

            return {
                "data_inserted": body,
                "message": "Success",
                "status_code": 200
            }, 200

        except Exception as e:
            return {
                       "data_inserted": [],
                       "message": f"{e}",
                       "status_code": 404
                   }, 404

    def patch(self):
        """
        This method will add user tag field
        :return:
        """

        try:
            parser.add_argument("document_id", type=int, required=True)
            parser.add_argument("tag", type=str, required=True)
            args = parser.parse_args()

            document_id = args["document_id"]
            tag = args["tag"]

            # Validate if document_id exist
            results = es.get(index="users", doc_type="document_id", id=document_id)

            results["_source"]["tag"] = tag  # Append the tag

            # Update the document
            es.index(index="users", doc_type="document_id", id=document_id, body=results["_source"])

            return {
                       "fs_metadata": results["_source"],
                       "message": "Success",
                       "status_code": 200
                   }, 200

        except Exception as e:
            return {
                       "fs_metadata": [],
                       "message": "Record not found!",
                       "status_code": 404
                   }, 404

    def delete(self):
        """
        This method will delete a particular document in ES
        :return:
        """
        try:
            parser.add_argument("document_id", type=int, required=True)
            args = parser.parse_args()

            document_id = args["document_id"]

            result = es.get(index="users", doc_type="document_id", id=document_id)
            if not result:
                raise Elasticsearch

            # Delete the record in ES
            es.delete(index="users", doc_type="document_id", id=document_id)

            return {
                       "document_id": document_id,
                       "message": "Success",
                       "status_code": 200
                   }, 200
        except Exception as e:
            return {
                       "document_id": document_id,
                       "message": "Record not found!",
                       "status_code": 404
                   }, 404
