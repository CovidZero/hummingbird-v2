import logging
import traceback
from app import app, db
from app import setup_database_migration
from apis.apis import load_apis
from werkzeug.exceptions import HTTPException


migrate = setup_database_migration(app, db)
load_apis(app)


@app.errorhandler(HTTPException)
def error_handler_http_exception(error):
    logging.info(f'HTTPException: {error}')
    if hasattr(error, 'code') and hasattr(error, 'description'):
        logging.debug(f'ERROR: {error.description}')
        return {'message': error.description}, error.code
    raise error


@app.errorhandler(Exception)
def error_handler_exception(error):
    logging.critical(f'SERVER ERROR: {error.args}')
    traceback.print_exc()
    raise error


if __name__ == '__main__':
    app.run()
