import os
import shutil
import subprocess
import orjson

from doc2req.model.api import Api
_CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

def from_src(
    src : str, 
    clear_generated_node_modules : bool = False
) -> Api:
    """
    run the parser file
    """

    install = ["npm", "install", "apidoc", "path"]
   
    proc = subprocess.Popen(
        install,
        cwd=_CURRENT_DIRECTORY,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )

    stdout, stderr = proc.communicate()
    print(stdout.decode("utf-8"))
    print(stderr.decode("utf-8"))

    execute = ["node", _CURRENT_DIRECTORY+"/parser.js", src]

    proc = subprocess.Popen(
        execute,
        cwd=os.getcwd(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
    )       

    stdout, stderr = proc.communicate()
    
    if clear_generated_node_modules:
        shutil.rmtree(os.path.join(os.getcwd(), "node_modules"), )

    json_obj = orjson.loads(stdout.decode("utf-8"))
    return Api(points=json_obj)