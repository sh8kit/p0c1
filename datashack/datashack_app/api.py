from python_terraform import *
from flask import Flask
import os
app = Flask(__name__)

def get_tf_vars_dict():
    return {"presto_host": os.environ.get("presto_host", "localhost"),
            "kafka_connect_host": os.environ.get("kafka_connect_host", "localhost"),
            "minio_host": os.environ.get("minio_host", "localhost"),
            "kafka_bootstarp_server": os.environ.get("kafka_bootstarp_server", "localhost:9092")}

@app.route('/')
def hello_world():
    
    if "terraform/environments/local" not in os.getcwd():
        os.chdir("terraform/environments/local")

    terraform = Terraform()
    terraform.init()
    
    return_code, stdout, stderr = terraform.apply(var=get_tf_vars_dict(),skip_plan=True)

    return {
        'code': return_code,
        'stdout': stdout,
        'stderr': stderr
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')