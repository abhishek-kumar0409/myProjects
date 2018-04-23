import subprocess

class ShellAction(object):
    def __init__(self):
        pass
    def execute(self, cmd):
        """
        This method accepts the command as an input and returns the console
        output of the executed command.
        :param cmd:
        :return:
        """
        try:
            print "Inside   cmd {}".format(cmd)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            std_out, std_err = process.communicate()
            exit_code = process.returncode

            print ("Command Exit Status: {}".format(str(exit_code)))
            if std_out is not None:
                print ("Output:\n {}".format(str(std_out)))

            if std_err is not None:
                print ("Error (if any):\n {}".format(str(std_err)))

            return (exit_code, std_out, std_err)

        except Exception as e:
            print ("Exception Caught at : {}".format(str(e)))

def main():
     saObj = ShellAction()
     code, std_out, std_err = saObj.execute(["aria", "service-template", "validate", "./medias/vnf-desc.yaml"])

if __name__ == "__main__":
     main()
