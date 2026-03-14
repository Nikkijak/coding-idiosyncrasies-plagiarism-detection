import os
import hashlib
import argparse

from .lex_tokenizer import tokenize, toText

HASH_HEX_CHARS = 8


def sha1_hash(text):
    hash_value = hashlib.sha1(text.encode("utf-8")).hexdigest()[-HASH_HEX_CHARS:]
    return int(hash_value, 16)


#Generating k-grams from normalized text.
def kgrams(text, k):
    token_list = list(text)
    n = len(token_list)
    kgram_list = []

    for i in range(n - k + 1):
        kgram = "".join(token_list[i:i + k])
        hash_value = sha1_hash(kgram)
        kgram_list.append((kgram, hash_value, i, i + k))

    return kgram_list


def min_index(arr):
    min_i = 0
    min_v = arr[0]

    for i in range(len(arr)):
        if arr[i] < min_v:
            min_v = arr[i]
            min_i = i

    return min_i


def fingerprints(arr, win_size=5):
    """Selecting representative hashes from the k-gram hash stream using the Winnowing algorithm. 
    This will reduce number of hashes stored while preserving matches
    between similar code fragments."""

    arr_len = len(arr)
    fingerprint_list = []

    if arr_len == 0 or win_size <= 0:
        return fingerprint_list

    if arr_len < win_size:
        return [min(arr)]

    previous_min = -1

    for i in range(arr_len - win_size + 1):
        window = arr[i:i + win_size]
        current_min = i + min_index(window)

        if current_min != previous_min:
            fingerprint_list.append(arr[current_min])
            previous_min = current_min

    return fingerprint_list


def hash_list(arr):
    return [x[1] for x in arr]


def process_text(filename, t=6, win_size=5):
    if t < 6:
        raise ValueError("t must be at least 6")

    tokens = tokenize(filename)
    clean_text = toText(tokens)

    kgram_list = kgrams(clean_text, k=t)
    fingerprint_list = fingerprints(hash_list(kgram_list), win_size=win_size)

    return fingerprint_list


def compare_fingerprints(f1_fingerprints, f2_fingerprints):
    #Comparing fingerprint sets using Jaccard similarity to estimate code overlap.

    set_f1 = set(f1_fingerprints)
    set_f2 = set(f2_fingerprints)

    intersection = set_f1.intersection(set_f2)
    union = set_f1.union(set_f2)

    if len(union) == 0:
        similarity = 0.0
    else:
        similarity = (len(intersection) / len(union)) * 100

    return similarity, list(intersection)


def get_all_files_in_directory(directory, file_extension=".java"):
    files = []

    if not os.path.isdir(directory):
        return files

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(file_extension):
                files.append(os.path.join(root, filename))

    return files


""" Run plagiarism detection across a dataset by comparing original,
    plagiarized, and non-plagiarized files using the fingerprint pipeline. 
    Remember to move this to a new file later."""
    
def process_dataset(
    dataset_path,
    output_file,
    t=6,
    win_size=5,
    threshold=30.0,
    file_extension=".java",
    original_dir="original",
    plagiarized_dir="plagiarized",
    clean_dir="non-plagiarized",
):
    similarity_results = []

    with open(output_file, "w", encoding="utf-8") as out:
        cases = os.listdir(dataset_path)

        for case in cases:
            case_path = os.path.join(dataset_path, case)

            if os.path.isdir(case_path):
                original_files = get_all_files_in_directory(
                    os.path.join(case_path, original_dir),
                    file_extension=file_extension,
                )
                plagiarized_files = get_all_files_in_directory(
                    os.path.join(case_path, plagiarized_dir),
                    file_extension=file_extension,
                )
                clean_files = get_all_files_in_directory(
                    os.path.join(case_path, clean_dir),
                    file_extension=file_extension,
                )

                for original_file in original_files:
                    out.write(f"Processing case: {case}\n")

                    original_fingerprints = process_text(
                        original_file,
                        t=t,
                        win_size=win_size,
                    )

                    for plagiarized_file in plagiarized_files:
                        plagiarized_fingerprints = process_text(
                            plagiarized_file,
                            t=t,
                            win_size=win_size,
                        )

                        similarity, matches = compare_fingerprints(
                            original_fingerprints,
                            plagiarized_fingerprints,
                        )

                        if similarity >= threshold:
                            out.write(
                                f"Similarity between {original_file} and {plagiarized_file}: {similarity:.2f}%\n"
                            )
                            out.write(f"Matching fingerprints: {matches}\n")
                            similarity_results.append((t, win_size, similarity))

                    for clean_file in clean_files:
                        clean_fingerprints = process_text(
                            clean_file,
                            t=t,
                            win_size=win_size,
                        )

                        similarity, matches = compare_fingerprints(
                            original_fingerprints,
                            clean_fingerprints,
                        )

                        if similarity >= threshold:
                            out.write(
                                f"Similarity between {original_file} and {clean_file}: {similarity:.2f}%\n"
                            )
                            out.write(f"Matching fingerprints: {matches}\n")
                            similarity_results.append((t, win_size, similarity))

                out.write("\n")

    return similarity_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Winnowing algorithm on a dataset.")
    parser.add_argument("dataset_path", type=str)
    parser.add_argument("output_file", type=str)
    parser.add_argument("--t", type=int, default=6)
    parser.add_argument("--win_size", type=int, default=5)
    parser.add_argument("--threshold", type=float, default=30.0)
    parser.add_argument("--file_extension", type=str, default=".java")
    parser.add_argument("--original_dir", type=str, default="original")
    parser.add_argument("--plagiarized_dir", type=str, default="plagiarized")
    parser.add_argument("--clean_dir", type=str, default="non-plagiarized")

    args = parser.parse_args()

    process_dataset(
        args.dataset_path,
        args.output_file,
        t=args.t,
        win_size=args.win_size,
        threshold=args.threshold,
        file_extension=args.file_extension,
        original_dir=args.original_dir,
        plagiarized_dir=args.plagiarized_dir,
        clean_dir=args.clean_dir,
    )