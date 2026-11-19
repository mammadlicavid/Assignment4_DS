
import sys
import xxhash

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
    open(f"{i}.txt", "w").close()

# The main loop continously asks for user input until a 
# KeyboardInterrupt or EOFError is raised
while True:
    try:
        text = input("Enter the string value: ")

        hash_value = xxhash.xxh64(text).intdigest() # Runs the xxhash algorithm on the input string and returns an integer digest
        hash_bucket = hash_value % n + 1

        with open(f"{hash_bucket}.txt", "a") as file:
            file.write(text)

        print(f"{text} added to {hash_bucket}.txt")

    except (KeyboardInterrupt, EOFError):
        print("\nClosing...")
        break
