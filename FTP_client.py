from ftplib import FTP

def ls(ftp):
    files = []
    ftp.dir(files.append)
    return files

def download_file(ftp, filename, local_filename):
    with open(local_filename, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, f.write)

def upload_file(ftp, filename, remote_filename):
    with open(filename, 'rb') as f:
        ftp.storbinary('STOR ' + remote_filename, f)

# Replace these with your FTP server details
ftp_server = '127.0.0.1'
ftp_username = 'izzat'
ftp_password = 'salam123'

# Connect to the FTP server
with FTP(ftp_server) as ftp:
    ftp.login(user=ftp_username, passwd=ftp_password)
    
    print("Files on FTP server:")
    files = ls(ftp)
    for file in files:
        print(file)

    # Download a file
    filename_to_download = 'sa'
    local_filename = 'as'
    download_file(ftp, filename_to_download, local_filename)
    print(f"Downloaded file '{filename_to_download}' to '{local_filename}'")

    # # Upload a file
    # filename_to_upload = 'file_to_upload.txt'
    # remote_filename = 'uploaded_file.txt'
    # upload_file(ftp, filename_to_upload, remote_filename)
    # print(f"Uploaded file '{filename_to_upload}' to FTP server as '{remote_filename}'")
