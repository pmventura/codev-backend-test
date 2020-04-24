from app.tests.base_test import BaseTest
import json
import requests
from config import Config


class TestAPI(BaseTest):

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

                req = requests.get(f"{Config.ELASTICSEARCH_URL}/users/_count").json()
                self.assertEqual(len(names), req["count"])

                response = client.get("/api/v1/users")
                res = json.loads(response.data)
                expected = {
                    "fs_metadata": fs_metadata,
                    "message": "Success",
                    "status_code": 200
                }
                self.assertEqual(200, response.status_code)
                self.assertCountEqual(expected["fs_metadata"], res["fs_metadata"])
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
                    "tag": "user_tag"
                }
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