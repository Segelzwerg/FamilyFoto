import os

from sqlalchemy.orm import mapper

from family_foto.models import db
from tests.base_test_case import BaseTestCase


class DbMigrateTestCase(BaseTestCase):
    """
    Tests the migration of the data base.
    """

    # pylint: disable=too-few-public-methods, no-member
    def test_db_migrate(self):
        """
        Tests the db migration.
        """
        meta_data = db.MetaData(bind=db.engine)
        table: db.Table = db.Table('test', meta_data, db.Column('id', db.Integer, primary_key=True))
        table.create()
        table.insert().values([1]).execute()

        class TestTable:
            """
            Empty table class.
            """

        mapper(TestTable, table)
        instance_path = os.path.join(os.path.dirname(__file__), 'instance')
        super().create_app()
        element = db.session.query(TestTable).all()[0]
        self.assertEqual(1, element.id)
