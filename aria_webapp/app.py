import os
from flask import Flask, request, redirect, url_for, jsonify, abort
from werkzeug import secure_filename
import parsers
import subprocess
from flask_restplus import Resource, Api
from shell_executor import ShellAction

app = Flask(__name__)
UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = set(['yaml', 'ml'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app, version='1.0', title='Aria Tosca Parser',
    description='API to validate Tosca Parser',
    contact = "abhishek.kumar0409@gmail.com",
    endpoint = "http://localhost:5000/upload/")

ns = api.namespace('aria_parser', description='Tosca Template Validation')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@ns.route('/upload/')
class my_file_upload(Resource):

    @api.expect(parsers.file_upload)
    def post(self):
        args = parsers.file_upload.parse_args()
        print "Args------->", args
        print "args dict --->", args['tosca_file'].__dict__
        if args['tosca_file'].mimetype == 'application/x-yaml':
            destination = os.path.join(app.config.get('UPLOAD_FOLDER'), 'medias/')
            print "Destination : {}".format(destination)
            if not os.path.exists(destination):
                os.makedirs(destination)

            filename = secure_filename(args['tosca_file'].filename)
            print "FileName ---> {} ".format(filename)

            tosca_file = '%s%s' % (destination, filename)
            print "Tosca File::: ", tosca_file

            args['tosca_file'].save(tosca_file)
            cmd = "aria service-template validate {}".format(tosca_file)
            print ("Executing {}".format(cmd))
            cmd_list = cmd.split(" ")
            executor = ShellAction()
            exit_code, std_out, std_err = executor.execute(cmd_list)
            if std_out is not None:
                print jsonify(str(std_out))
            if std_err is not None:
                print jsonify(str(std_err))

        else:
            abort(404)

        if(exit_code != 0):
            return {'status': 'Validation Test Failed!'}
        else:
            return {'status': 'Validation Test Success!'}

if __name__ == '__main__':
    app.run(debug=True)


