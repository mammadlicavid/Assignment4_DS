
import os
import sys
import xxhash

import json

# Make sure the 3 argument requirement is met (filename, n, s)
if len(sys.argv) != 3:
    print("Correct syntax is 'python hash_app.py <n> <s>' ")
    sys.exit()


# Initialize the n and s values from command line arguments (as integers)
n = int(sys.argv[1])
s = int(sys.argv[2])

# Condition for negative values of n and s
if n <= 0 or s <= 0:
    print("n and s both have to be positive integers.")
    sys.exit()


for i in range(1, n + 1): # account for neglected last number in range
    open(f"{i}.txt", "a").close()

# Load previous bucket links from a JSON file if it exists, 
# otherwise initialize an empty dict
if os.path.exists("bucket_links.json"):
    with open("bucket_links.json", "r") as json_file:
        bucket_links = json.load(json_file) 
else:
    bucket_links = {} 

for i in range(1, n + 1):
    if str(i) not in bucket_links:
        # Initialize the overflow count for each bucket to 0 if it doesn't exist in the loaded data
        bucket_links[str(i)] = 0  


#  The main loop continously asks for user input until a 
# KeyboardInterrupt or EOFError is raised
while True:
    try:
        text = input("Enter the string value: ")

        hash_value = xxhash.xxh64(text.encode("utf-8")).intdigest() # Runs the xxhash algorithm on the input string and returns an integer digest
        hash_bucket = hash_value % n + 1

        # Determine where the next string goes
        # If the bucket is empty, it goes to the main file.
        # If not, it goes to the overflow file.
        overflow_num = bucket_links[str(hash_bucket)] 
        if overflow_num == 0:
            filename = f"{hash_bucket}.txt"
        else:
            filename = f"{hash_bucket}_overflow_{overflow_num}.txt"

        # Kepp track of the text that is not yet written to the file
        remaining_text = text 

        while remaining_text:
            # Read the current contents of the file
            with open(filename, "r") as file:
                current_text = file.read()

            available_space = s - len(current_text)

            # If the available space is greater than or equal to the length of the remaining text, write it to the file and break the loop
            if available_space == 0:
                overflow_num += 1
                bucket_links[str(hash_bucket)] = overflow_num
                filename = f"{hash_bucket}_overflow_{overflow_num}.txt"
                available_space = s  # Reset available space for the new overflow file

            # Slice and write the remaining text to the file
            part = remaining_text[:available_space]

            with open(filename, "a") as file:
                file.write(part)

            remaining_text = remaining_text[len(part):]  # Update the remaining text

        print(f"{text} is successfully added to {filename}")

        # Save the bucket_links to a JSON file for future reference
        with open("bucket_links.json", "w") as json_file:
            json.dump(bucket_links, json_file)

    # Handle KeyboardInterrupt and EOFError to exit the program peacefully
    except (KeyboardInterrupt, EOFError):
        print("\nClosing...")
        break
