# Duplicate Killer
A Python script to remove duplicate files from a directory and subdirectories in safe and dangerous modes.

# Usage
`python3 ./duplicate-killer.py <src_dir> <dst_dir> <rename>`
* `src_dir` - Source directory to search for duplicate files.
* `dst_dir` - Destination directory to be free of duplicate files.
* `rename` - If true, files are renamed to the computed hash sum. If false, the original name is preserved.

The "safe" mode to delete duplicate files is to use a separate source and destination directory. This allows you to examine the results before the duplicate files are deleted.

The "dangerous" mode is to set the destination directory to be the source directory. If this is done, then a temporary directory is used as an intermediate location before deleting the duplicate files automatically. This is more convenient, but there is no going back once the process is done.
