import subprocess


def sendmail(idea_name, created_by, createdat):
    # Define the path to your Bash script
    # Replace with the actual path to your script
    bash_script_path = "/data/fastapi/mail.sh"

    # Arguments to pass to the Bash script
    emp_id = "I355833"  # Replace with the desired Employee ID
    ideaname = idea_name  # Replace with the desired Idea Name
    createdby = created_by
    created_at = createdat
    # Build the command to execute the Bash script with arguments
    command = [bash_script_path, emp_id, ideaname, createdby, created_at]

    try:
        # Run the Bash script from Python
        result = subprocess.run(
            command, capture_output=True, text=True, check=True)

    # Print the script's standard output
        print("Script Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        # If the script returns a non-zero exit code, handle the error
        print(f"Script Error (Exit Code {e.returncode}):")
        print(e.stderr)
    except Exception as e:
        # Handle other exceptions, if any
        print(f"An error occurred: {e}")
