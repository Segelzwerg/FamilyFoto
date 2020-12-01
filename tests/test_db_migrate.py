import os

from sqlalchemy.orm import mapper

import family_foto
from tests.base_test_case import BaseTestCase
from family_foto.models import db


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
        _ = family_foto.create_app({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_TRACK_MODIFICATIONS': True,
            # Since we want our unit tests to run quickly
            # we turn this down - the hashing is still done
            # but the time-consuming part is left out.
            'HASH_ROUNDS': 1
        }, instance_path)
        element = db.session.query(TestTable).all()[0]
        self.assertEqual(1, element.id)
