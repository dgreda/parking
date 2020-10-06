# Flask settings
FLASK_SERVER_NAME = '0.0.0.0:5000'
FLASK_DEBUG = False  # Do not use debug mode in production

# Flask-Restx settings
RESTX_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTX_VALIDATE = True
RESTX_MASK_SWAGGER = False
ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_TRACK_MODIFICATIONS = False
