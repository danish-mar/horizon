import os
import subprocess

# Define the path to your Flask application
flask_app_dir = '/home/keqing/PycharmProjects/Horizon'

# Change the current working directory to the Flask app directory
os.chdir(flask_app_dir)

# Run the Flask application
subprocess.run(['flask', 'run'])
