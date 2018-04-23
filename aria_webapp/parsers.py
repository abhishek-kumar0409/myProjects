#parsers.py
import werkzeug
from flask_restplus import reqparse

file_upload = reqparse.RequestParser()
file_upload.add_argument('tosca_file',
                         type=werkzeug.datastructures.FileStorage,
                         location='files',
                         required=True,
                         help='Tosca -> a yaml file')
