from subprocess import check_output, CalledProcessError
import logging
from tempfile import TemporaryFile

## Code Compilation
COMPILED_SRCS = "/home/vagrant/dev/fabric_manager/switch_config/compiled_srcs/"
JSON_P4_COMPILED = COMPILED_SRCS + "compiled.json"
P4_COMPILED = COMPILED_SRCS + "compiled.p4"

## Initialization of Switch
BMV2_PATH = "/home/vagrant/bmv2"
BMV2_SWITCH_BASE = BMV2_PATH + "/targets/simple_switch"

SWITCH_PATH = BMV2_SWITCH_BASE + "/simple_switch"
CLI_PATH = BMV2_SWITCH_BASE + "/sswitch_CLI"
THRIFTPORT = 22222

P4_COMMANDS = COMPILED_SRCS + "commands.txt"
logging.getLogger(__name__)


def send_commands_to_dp(cli_path, p4_json_path, thrift_port, p4_commands):
    cmd = [cli_path, p4_json_path, str(thrift_port)]
    logging.info(" ".join(cmd))
    P4_COMMANDS = "\n".join(p4_commands)
    logging.info(P4_COMMANDS)
    get_in(cmd, P4_COMMANDS)

def get_out(args):
    with TemporaryFile() as t:
        try:
            out = check_output(args, stderr=t, shell=True)
            logging.debug("SUCCESS: " + str(args) + ",0 ," + str(out))
            return True, out
        except CalledProcessError as e:
            t.seek(0)
            logging.error("ERROR: " + str(args) + str(e.returncode) + t.read())
            return False, t.read()


def write_to_file(path, content):
    with open(path, 'w') as fp:
        fp.write(content)


def get_in(args, input):
    with TemporaryFile() as t:
        try:
            t.write(input)
            out = check_output(args, stdin=t, shell=False)
            logging.debug("SUCCESS: " + str(args) + ",0 ," + str(out))
            return True, out
        except CalledProcessError as e:
            t.seek(0)
            logging.error("ERROR: " + str(args) + str(e.returncode) + t.read())
            return False, t.read()