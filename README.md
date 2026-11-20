# Assignment 4 — Hashing Application

## Description

This project implements a file-based hashing application in Python. It accepts strings from the user, calculates their hash values using the xxHash algorithm, and stores them in text files called buckets.

Each bucket has a maximum capacity. When a bucket becomes full, the program creates overflow files to store additional characters.

## Requirements

- Python 3
- xxhash library

Install the required library (Pip has to be installed and configured):

```bash
python -m pip install xxhash
```

## How to Run

Run the application using:

```bash
python hash_app.py n s
```

Where:
- `n` is the number of primary buckets.
- `s` is the maximum number of characters allowed in each bucket file.

Example:

```bash
python hash_app.py 3 5
```

This creates 3 primary buckets, each with a maximum capacity of 5 characters.

The program continuously accepts strings until the user presses `Ctrl+C` to close the program.

## Hashing Algorithm

The application uses **xxHash64**, a fast, non-cryptographic hashing algorithm.

Before hashing, each input string is encoded using UTF-8.

The hash value is converted into a bucket number using:

```python
hash_bucket = hash_value % n + 1
```

The mod operation ensures that the selected bucket is between `1` and `n`.

## Bucket Storage and Overflow

Primary bucket files are named:

```text
1.txt
2.txt
3.txt
```

When a bucket reaches its capacity, additional files are created:

```text
1_overflow_1.txt
1_overflow_2.txt
```

If a string cannot fit entirely into the current file, the program splits it into smaller parts and stores them across the bucket and its overflow files.

Strings are stored without separators.

## Overflow Reference Mechanism

The application uses a Python dictionary named `bucket_links` to track the latest overflow file for each bucket.

These references are saved in `bucket_links.json`.

Example:

```json
{
    "1": 2,
    "2": 0,
    "3": 1
}
```

In this example:
- Bucket 1 has two overflow files.
- Bucket 2 has no overflow files.
- Bucket 3 has one overflow file.

When the program restarts, it loads the saved JSON references and continues writing to the latest overflow file.

Existing bucket contents are preserved.

## Stopping the Program

Press `Ctrl+C` to stop the application.

The program handles the interruption and exits gracefully.