import mailbox
import os

# Path to the mbox file
mbox_file = '1565678501.M823588P2633.p3plcpnl0574.prod.phx3.secureserver.net,S=24401,W=24562_2,S'

# Directory to save the .eml files
output_directory = 'eml_files/'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Open the mbox file
mbox = mailbox.mbox(mbox_file)

# Iterate through each message in the mbox file
for i, message in enumerate(mbox):
    # Create a file name for the .eml file based on the message number
    eml_file = os.path.join(output_directory, f'message_{i}.eml')

    # Write the message content to the .eml file
    with open(eml_file, 'w') as eml:
        eml.write(str(message))
