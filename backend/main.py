from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os
import json
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TERRAFORM_DIR = os.path.join(os.path.dirname(__file__), 'infrastructure')
STATE_FILE = os.path.join(TERRAFORM_DIR, 'terraform.tfstate')

class InstanceConfig(BaseModel):
    instance_type: str
    count: int = 1

def run_terraform(command: str, variables: dict = None):
    try:
        cmd = ['terraform', command, '-auto-approve']
        if variables:
            for k, v in variables.items():
                cmd.extend(['-var', f'{k}={v}'])
        
        result = subprocess.run(
            cmd,
            cwd=TERRAFORM_DIR,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            raise HTTPException(
                status_code=400,
                detail=f"Terraform error: {result.stderr}"
            )
            
        return result.stdout
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/instances/")
async def create_instances(config: InstanceConfig):
    # Initialize Terraform
    subprocess.run(['terraform', 'init'], cwd=TERRAFORM_DIR, check=True)
    
    # Apply configuration
    output = run_terraform('apply', {
        'instance_type': config.instance_type,
        'instance_count': config.count
    })
    
    # Get output
    result = subprocess.run(
        ['terraform', 'output', '-json'],
        cwd=TERRAFORM_DIR,
        capture_output=True,
        text=True
    )
    
    return {
        "message": "Instances created",
        "output": output,
        "public_ips": json.loads(result.stdout)['public_ips']['value']
    }

@app.get("/instances/")
async def list_instances():
    if not Path(STATE_FILE).exists():
        return {"instances": []}
        
    result = subprocess.run(
        ['terraform', 'show', '-json', STATE_FILE],
        cwd=TERRAFORM_DIR,
        capture_output=True,
        text=True
    )
    
    tf_data = json.loads(result.stdout)
    instances = []
    
    if 'values' in tf_data:
        for instance in tf_data['values']['root_module']['resources']:
            if instance['type'] == 'aws_instance':
                instances.append({
                    "id": instance['values']['id'],
                    "public_ip": instance['values']['public_ip'],
                    "state": instance['values']['instance_state']
                })
    
    return {"instances": instances}

@app.post("/instances/destroy")
async def destroy_instances():
    output = run_terraform('destroy')
    return {"message": "Instances destroyed", "output": output}