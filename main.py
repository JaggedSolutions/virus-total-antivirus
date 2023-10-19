# Import the requests library
import requests

# Import the hashlib library
import hashlib

# Import the sys library
import sys

# Import the tkinter library
import tkinter as tk

# Import the os library
import os

# Import the time library
import time

# Define the VirusTotal API key
api_key = "APIKEY"

# Define the headers for the request
headers = {"x-apikey": api_key}


# Define a function to get the file report by hash
def get_file_report_by_hash(file_hash):
    # Define the VirusTotal API endpoint for file report
    file_report_url = "https://www.virustotal.com/api/v3/files/" + file_hash

    # Define the headers for the request
    headers = {"x-apikey": api_key}

    # Send a GET request to the file report endpoint
    file_report_response = requests.get(file_report_url, headers=headers)

    # Check the status code of the response
    if file_report_response.status_code == 200:
        # The file report was found
        # Parse the JSON response
        file_report_data = file_report_response.json()
        # Get the file name from the response
        # print(file_report_data)
        # file_name = file_report_data["data"]["attributes"]["names"][0]
        file_name = os.path.basename(file_path)

        # Get the number of virus detections from the response
        detections = file_report_data["data"]["attributes"]["last_analysis_stats"]["malicious"]
        # Get the total number of antiviruses from the response
        
        # total = file_report_data["data"]["attributes"]["last_analysis_stats"]["total"]
        # total = file_report_data["data"]["attributes"]["last_analysis_stats"]["confirmed-timeout"]
        total = file_report_data["data"]["attributes"]["last_analysis_stats"]["undetected"]

        # Return the file name, detections and total as a tuple
        return (file_name, detections, total)
    elif file_report_response.status_code == 404:
        # The file report was not found
        # Return None
        return None
    else:
        # The file report request failed or there was an error
        print("Could not get the file report")
        sys.exit(1)

# Define a function to upload a file and get the analysis report by ID
def upload_file_and_get_analysis_report(file_path):
    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Read the file content
        file_content = f.read()
    
    # Get the file size in bytes
    file_size = len(file_content)

    if file_size <= 32 * 1024 * 1024:
        # The file size is less than or equal to 32 MB
        # Define the VirusTotal API endpoint for file upload
        file_upload_url = "https://www.virustotal.com/api/v3/files"
        # Define the files for the request
        files = {"file": (file_path, open(file_path, "rb"))}
        # Send a POST request to the file upload endpoint
        file_upload_response = requests.post(file_upload_url, headers=headers, files=files)
        # Check the status code of the response
        if file_upload_response.status_code == 200:
            # The file upload was successful
            # Parse the JSON response
            file_upload_data = file_upload_response.json()
            # Get the analysis ID from the response
            analysis_id = file_upload_data["data"]["id"]
            # Define the VirusTotal API endpoint for analysis report
            analysis_report_url = "https://www.virustotal.com/api/v3/analyses/" + analysis_id
            
            # Wait for some time for the analysis to complete
            time.sleep(10)
            
            # Send a GET request to the analysis report endpoint
            analysis_report_response = requests.get(analysis_report_url, headers=headers)
            # Check the status code of the response
            if analysis_report_response.status_code == 200:
                # The analysis report was found
                # Parse the JSON response
                analysis_report_data = analysis_report_response.json()
                # Get the file name from the response
                
                # file_name = analysis_report_data["meta"]["file_info"]["name"]
                file_name = os.path.basename(file_path)
                
                # Get the number of virus detections from the response
                detections = analysis_report_data["data"]["attributes"]["stats"]["malicious"]
                # Get the total number of antiviruses from the response
                total = analysis_report_data["data"]["attributes"]["last_analysis_stats"]["undetected"]
                print(total.json(indent=4))
                # Return the file name, detections and total as a tuple
                return (file_name, detections, total)
            else:
                # The analysis report was not found or there was an error
                print("Could not get the analysis report")
                sys.exit(1)
        else:
            # The file upload failed or there was an error
            print("Could not upload the file")
            sys.exit(1)
    elif file_size <= 650 * 1024 * 1024:
        # The file size is greater than 32 MB and less than or equal to 650 MB
        # Define the VirusTotal API endpoint for upload URL request
        upload_url_request_url = "https://www.virustotal.com/api/v3/files/upload_url"
        # Send a GET request to the upload URL request endpoint
        upload_url_request_response = requests.get(upload_url_request_url, headers=headers)
        # Check the status code of the response
        if upload_url_request_response.status_code == 200:
            # The upload URL request was successful
            # Parse the JSON response 
            upload_url_request_data = upload_url_request_response.json()
            # Get the upload URL from the response
            upload_url = upload_url_request_data["data"]
            # Define the files for the request
            files = {"file": (file_path, open(file_path, "rb"))}
            # Send a POST request to the upload URL
            upload_url_response = requests.post(upload_url, headers=headers, files=files)
            # Check the status code of the response
            if upload_url_response.status_code == 200:
                # The file upload was successful
                # Parse the JSON response
                upload_url_data = upload_url_response.json()
                # Get the analysis ID from the response
                analysis_id = upload_url_data["data"]["id"]
                # Define the VirusTotal API endpoint for analysis report
                analysis_report_url = "https://www.virustotal.com/api/v3/analyses/" + analysis_id
                
                # Wait for some time for the analysis to complete
                time.sleep(60)
                
                # Send a GET request to the analysis report endpoint
                analysis_report_response = requests.get(analysis_report_url, headers=headers)
                # Check the status code of the response
                if analysis_report_response.status_code == 200:
                    # The analysis report was found
                    # Parse the JSON response
                    analysis_report_data = analysis_report_response.json()
                    # Get the file name from the response
                    file_name = os.path.basename(file_path)
                    # Get the number of virus detections from the response
                    detections = analysis_report_data["data"]["attributes"]["stats"]["malicious"]
                    # Get the total number of antiviruses from the response
                    total = analysis_report_data["data"]["attributes"]["last_analysis_stats"]["undetected"]
                    # Return the file name, detections and total as a tuple
                    return (file_name, detections, total)
                else:
                    # The analysis report was not found or there was an error
                    print("Could not get the analysis report")
                    sys.exit(1)
            else:
                # The file upload failed or there was an error
                print("Could not upload the file")
                sys.exit(1)
        else:
            # The upload URL request failed or there was an error
            print("Could not get the upload URL")
            sys.exit(1)
    else:
        # The file size is greater than 650 MB
        print("The file is too large to be uploaded to VirusTotal")
        sys.exit(1)

# Define a function to delete the file and exit the program
def delete_file():
    try:
        os.remove(file_path)
        print(f"Deleted {file_path}")
    except OSError as e:
        print(f"Could not delete {file_path}: {e}")
    finally:
        sys.exit(0)

# Define a function to exit the program without deleting the file
def exit_program():
    sys.exit(0)

# Define a function to create a window to display the virus report and the options
def create_window(file_name, detections, total):
    # Create a tkinter window to display the virus report and the options
    window = tk.Tk()
    window.title("Virus Report")
    window.geometry("300x200")

    # Create a label to show the file name and the virus report
    label = tk.Label(window, text=f"{file_name}: {detections}/{total}", font=("Arial", 16))
    label.pack(pady=20)

    # Create a button to delete the file and exit the program
    delete_button = tk.Button(window, text="Delete File", command=delete_file, bg="red", fg="white")
    delete_button.pack(pady=10)

    # Create a button to exit the program without deleting the file
    exit_button = tk.Button(window, text="Exit Program", command=exit_program, bg="green", fg="white")
    exit_button.pack(pady=10)

    # Start the window main loop
    window.mainloop()

# Check if a file path is given as an argument
if len(sys.argv) < 2:
    print("Usage: python main.py <file_path>")
    sys.exit(1)

# Extract the file path from the command line argument
file_path = sys.argv[1]

# Open the file in binary mode and calculate its hash
with open(file_path, "rb") as f:
    file_hash = hashlib.sha256(f.read()).hexdigest()

# Try to get the file report by hash
file_report = get_file_report_by_hash(file_hash)

# Check if the file report was found
if file_report is not None:
    # Unpack the file report tuple
    file_name, detections, total = file_report
else:
    # Try to upload the file and get the analysis report by ID
    analysis_report = upload_file_and_get_analysis_report(file_path)

    # Check if the analysis report was found
    if analysis_report is not None:
        # Unpack the analysis report tuple
        file_name, detections, total = analysis_report
    else:
        # No report was found or there was an error
        print("Could not get any report")
        sys.exit(1)

# Create a window to display the virus report and the options
if detections > 0:
    create_window(file_name, detections, total)
