from unittest import TestCase
from app import create_app
from elasticsearch import Elasticsearch


class BaseTest(TestCase):
    """
    BaseTest class
    """

    def setUp(self) -> None:
        """
        This method will run once per each test method
        :return:
        """

        app = create_app()
        self.app = app.test_client
        self.app_context = app.app_context
        self.es = Elasticsearch(app.config["ELASTICSEARCH_URL"])

    def tearDown(self) -> None:
        pass
        app = create_app()
        es = Elasticsearch(app.config['ELASTICSEARCH_URL'])
        # Delete indices
        es.indices.delete(index="users", ignore=[400, 404])
