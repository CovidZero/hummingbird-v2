import os
import sys
from unittest.loader import TestLoader
from unittest import TextTestRunner
from main import app, db


def main():
    with app.app_context():
        if os.getenv('FLASK_ENV') not in ['testing']:
            raise Exception('TESTS IS ALLOWED TO RUN ONLY END TESTING MODE')
        try:
            os.remove('src/test_data/test.db')
        except IOError:
            print('Not found test db')
        db.create_all()
        suite = TestLoader().discover(
            'tests',
            pattern='test_*.py',
            top_level_dir=os.environ['PYTHONPATH'].split(os.pathsep)[0]
        )
        return TextTestRunner(verbosity=1).run(suite)


def clear_db(_db):
    if os.getenv('FLASK_ENV') not in ['testing']:
        raise Exception('TESTS IS ALLOWED TO RUN ONLY END TESTING MODE')
    db.session.rollback()
    for table in reversed(_db.metadata.sorted_tables):
        _db.session.execute(table.delete())
    _db.session.commit()


if __name__ == '__main__':
    result = main()
    if not result.wasSuccessful():
        sys.exit(1)
