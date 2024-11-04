# Tf_deploy.py is the python file for deploying the terraform code
# These functions are called by function in Server.py when client sends a request to deploy the terraform code
"""
The functions in this file are responsible for the following:
1. Deploying the terraform code for a given account
2. Creating a new workspace for the account: A workspace can seperate the resources for different accounts
3. Deleting the workspace for the account
4. Ensuring the workspace exists
5. Running the terraform commands and writing the output to a file
"""

import subprocess
import os
from datetime import datetime
import asyncio
from StopEvent import StopEvent
from Tf_output import filter_terraform_output
from S3_handler import periodic_s3_upload, S3Handler
from CommandResult import CommandResult

stop_event = StopEvent()
s3 = S3Handler()

async def write_to_file(output_file, line, system_status: CommandResult, account_id):
    # write the filtered msg to the file and print it
    with open(output_file, 'a') as f:
        filtered_line = filter_terraform_output(line)
        system_status.set_output(filtered_line)
        f.write(f"{filtered_line}\n")
        f.flush() # flush the buffer
        print(f"[Account {account_id}] {line}", flush=True)

# run the terraform command and write into file
async def rw_terraform_command(cmd, output_file, account_id, system_status: CommandResult):
    output = [] # store the output of the command
    # run the command and keep the execution output msg
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT
    )

    while True:
        line = await process.stdout.readline() # get the output after executing  the command line by line
        # check if the line is empty
        if not line:
            break
        line = line.decode().strip()
        output.append(line)
        write_to_file(output_file, line, system_status, account_id) # write the filtered msg to the file
        await process.wait() # wait for the process to complete

        # check if the command is executed successfully
        if process.returncode != 0:
            await asyncio.sleep(10)
            raise subprocess.CalledProcessError(process.returncode, cmd, '\n'.join(output))
        
    return '\n'.join(output)

 # Before deleting the workspace, we need to destroy the resources in the workspace   
async def destroy_resources_in_workspace(terraform_dir, workspace_name, output_file, account_id, system_status: CommandResult):
    # try to select the existing workspace for client and destroy the resources in it
    try:
        await rw_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "select", workspace_name],
            output_file,
            account_id,
            system_status
        )
        print(f"Attempting to destroy resources in workspace {workspace_name}...")
        await rw_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "destroy", "-auto-approve"],
            output_file,
            account_id,
            system_status
        )
        print(f"Successfully destroyed all resources in workspace {workspace_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to destroy resources in workspace {workspace_name}")
        print("Terraform output:")
        print(e.output)
        return False
    
    # select the default workspace if the command fails
    finally:
        await rw_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "select", "default"],
            output_file,
            account_id,
            system_status
        )

async def delete_workspace(terraform_dir, workspace_name, output_file, account_id, system_status: CommandResult):
    try:
        # checlout to the default workspace before deleting the workspace. We cannot delete the workspace if we are in it
        await rw_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "select", "default"],
            output_file,
            account_id,
            system_status
        )

        # destroy the resources in the workspace before deleting it
        destroy_success = await destroy_resources_in_workspace(terraform_dir, workspace_name, output_file, account_id, system_status)
        if not destroy_success:
            print("Failed to destroy resources in workspace. Proceeding with deletion anyway.")
        
        delete_output = await rw_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "delete", "-force", workspace_name],
            output_file,
            account_id,
            system_status
        )
        print(f"Workspace deletion output: {delete_output}")

        # check if the workspace is deleted successfully
        if f"Deleted workspace \"{workspace_name}\"" in delete_output: 
            print(f"Successfully deleted workspace '{workspace_name}'")
            return True
        else:
            print(f"Failed to delete workspace '{workspace_name}'")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error deleting workspace: {e}")
        print(f"Command output: {e.output}")
        return False



# ensure whether the workspace exist 
async def ensure_workspace(terraform_dir, workspace_name, output_file, account_id, system_status: CommandResult):
    try:
        os.chdir(terraform_dir)
        list_output = await rw_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "list"],
            output_file,
            account_id,
            system_status   
        )
        if workspace_name in list_output:
            print(f"Workspace '{workspace_name}' exists.")
            return True
    except subprocess.CalledProcessError as e:
        print(f"Error managing workspace: {e}")
        return False

async def create_new_workspace(terraform_dir, workspace_name, output_file, account_id, system_status: CommandResult):
    try:
        create_output = await rw_terraform_command(
            ["terraform", "-chdir=" + terraform_dir, "workspace", "new", workspace_name],
            output_file,
            account_id,
            system_status
        )
        print(f"Workspace creation output: {create_output}")            
        if "Created and switched to workspace" in create_output:
            print(f"Successfully created new workspace '{workspace_name}'")
            return True
        else:
            print(f"Failed to create workspace '{workspace_name}'")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error creating workspace: {e}")
        return False

# deploying the tf code and returning the msg for rendering
async def terraform_deploy(account_id, sys_status: CommandResult):
    output_file = f"terraform_output_{account_id}.txt"
    bucket_name = "kg-for-test"
    s3_key = f"user_data/{account_id}/{output_file}"
    workspace_name = f"customer_{account_id}"
    terraform_dir = f"/home/ec2-user/customers/{account_id}"

    try:
        if not os.path.exists(terraform_dir):
            raise FileNotFoundError(f"Terraform directory not found: {terraform_dir}")
        if not os.path.exists(os.path.join(terraform_dir, 'main.tf')):
            raise FileNotFoundError(f"main.tf not found in: {terraform_dir}")
        try:
            # check if the workspace exists, if not create a new workspace
            # because we cannot select the existing workspace and execute the terraform commands during the project development phase
            if not await ensure_workspace(terraform_dir, workspace_name, output_file, account_id, sys_status):
                await create_new_workspace(terraform_dir, workspace_name, output_file, account_id, sys_status)  
            else:
                await delete_workspace(terraform_dir, workspace_name, output_file, account_id, sys_status)
                await create_new_workspace(terraform_dir, workspace_name, output_file, account_id, sys_status)  
        except subprocess.CalledProcessError as e:
            print(f"Error for workspace preprocessing: {e}")
        try:
            select_result = await rw_terraform_command(
                ["terraform", "-chdir=" + terraform_dir, "workspace", "select", workspace_name],
                output_file,
                account_id,
                sys_status
            )
            print(f"Selected workspace: {select_result}")
        except subprocess.CalledProcessError as e:
            print(f"Error selecting workspace: {e}")

        # deploy the terraform code: init, apply
        commands = [
            ["terraform", "-chdir=" + terraform_dir, "init"],
            ["terraform", "-chdir=" + terraform_dir, "apply", "-auto-approve"]
        ]

        global stop_event
        upload_task = asyncio.create_task(
            s3.periodic_s3_upload(terraform_dir, output_file, bucket_name, s3_key, stop_event)
        )

        for cmd in commands:
            await rw_terraform_command(cmd, output_file, account_id, sys_status)

        stop_event.set()
        upload_task.cancel()
        try:
            await upload_task
        except asyncio.CancelledError:
            pass
        print(f"Terraform apply completed successfully for account {account_id} in workspace: {workspace_name}")
        sys_status.set_death() # stop this task if the terraform apply is completed, or it will keep running
        return {
            "status": "success",
            "data": {
                "deployedAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "outputLocation": f"s3://{bucket_name}/{s3_key}"
            }
        }, 200
    except subprocess.CalledProcessError as e:
        error_message = f"Terraform command failed for account {account_id}: {str(e)}"
        print(error_message)
        return {"status": "error", "message": error_message}, 500
    except Exception as e:
        error_message = f"An error occurred for account {account_id}: {str(e)}"
        print(error_message)
        return {"status": "error", "message": error_message}, 500