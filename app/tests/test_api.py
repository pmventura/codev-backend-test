from app.tests.base_test import BaseTest
import json
import requests
from datetime import datetime
import time
from config import Config


class TestAPI(BaseTest):

    def test_create_fs_metadata(self):
        """
        This method will test the creation of fs metadata
        :return:
        """
        with self.app() as client:
            with self.app_context():

                today = datetime.now()

                data = {
                    "file_path": "users.json"
                }
                response = client.post("/api/v1/users", data=data)
                res = json.loads(response.data)

                expected = {
                    "data_inserted": {
                        "file_path": data["file_path"],
                        "extension": ".json",
                        "date_ingested": res["data_inserted"]["date_ingested"]
                    },
                    "message": "Success",
                    "status_code": 200
                }

                self.assertEqual(200, response.status_code)
                self.assertIn("file_path", res["data_inserted"])
                self.assertIn("extension", res["data_inserted"])
                self.assertIn("date_ingested", res["data_inserted"])
                self.assertDictEqual(expected, res)

                data = {
                    "file_path": "/data"
                }
                response = client.post("/api/v1/users", data=data)
                res = json.loads(response.data)
                self.assertEqual(404, response.status_code)
                self.assertEqual("Path doesn't exist", res["message"])

    def test_get_all_documents(self):
        """
        This method will test extracting documents
        :return:
        """

        with self.app() as client:
            with self.app_context():

                # Initialised data
                fs_metadata = []
                names = ["Jane Doe", "John Doe", "Martin Stewart", "Donald Mccain"]
                for i in range(len(names)):
                    data = {
                        "document_id": i+1,
                        "display_name": names[i]
                    }
                    fs_metadata.append(data)
                    self.es.index(index="users", id=data["document_id"], doc_type="document_id", body=data)

                response = client.get("/api/v1/users")
                res = json.loads(response.data)
                expected = {
                    "fs_metadata": fs_metadata,
                    "message": "Success",
                    "status_code": 200
                }

                self.assertEqual(200, response.status_code)
                self.assertEqual(expected["message"], res["message"])

    def test_add_user_tag(self):
        """
        This method will test adding user tag field
        :return:
        """

        with self.app() as client:
            with self.app_context():

                data = {
                    "document_id": 1,
                    "display_name": "Pablo Escobar",
                    "tag": "user_tag"
                }
                # Add record to ES before patching
                self.es.index(index="users", id=data["document_id"], doc_type="document_id", body=data)

                response = client.patch("/api/v1/users", data=data)
                res = json.loads(response.data)

                data["display_name"] = res["fs_metadata"]["display_name"]
                expected = {
                    "fs_metadata": data,
                    "message": "Success",
                    "status_code": 200
                }

                self.assertEqual(200, response.status_code)
                self.assertIsNotNone(res)
                self.assertDictEqual(expected, res)

                # Assert with no record found
                data["document_id"] = 123456 # Set some random id
                response = client.patch("/api/v1/users", data=data)
                res = json.loads(response.data)

                expected = {
                    "fs_metadata": [],
                    "message": "Record not found!",
                    "status_code": 404
                }

                self.assertEqual(404, response.status_code)
                self.assertDictEqual(expected, res)

    def test_delete_document(self):
        """
        This method will test deleting a document
        :return:
        """

        with self.app() as client:
            with self.app_context():
                data = {
                    "document_id": 1
                }
                self.es.index(index="users", id=data["document_id"], doc_type="document_id", body=data)

                response = client.delete("/api/v1/users", data=data)
                res = json.loads(response.data)
                expected = {
                    "document_id": data["document_id"],
                    "message": "Success",
                    "status_code": 200
                }
                self.assertEqual(200, response.status_code)
                self.assertDictEqual(expected, res)

                # Assert with no record found
                response = client.delete("/api/v1/users", data=data)
                res = json.loads(response.data)
                expected = {
                    "document_id": data["document_id"],
                    "message": "Record not found!",
                    "status_code": 404
                }
                self.assertEqual(404, response.status_code)
                self.assertDictEqual(expected, res)