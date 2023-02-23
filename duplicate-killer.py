from scraping_utils.scraping_utils import compute_file_hashes
import os
import shutil
import hashlib
from tempfile import TemporaryDirectory
from sys import stdout, argv


"""
Driver function. Save only unique files from a source directory into a destination directory.
@param src - Source to query.
@param dst - Destination free of duplicates. If equal, a temporary directory is used.
@param rename - Boolean to rename the files to the computed hash sum.
@param move - Boolean to move the files instead of copying them. Much faster, but interrupts could cause corruption.
"""
def main(src, dst, rename, move):
    # Remove any the trailing separator from the source and destination
    if(src.endswith(os.sep)):
        src = src[:-1]
    if(dst.endswith(os.sep)):
        dst = dst[:-1]
    
    # If the source and destination are equal, take note and use a tmp directory.
    is_tmp = (src == dst)
    if(is_tmp):
        dst = TemporaryDirectory().name
        os.mkdir(dst)
        stdout.write('[main] INFO: Removing duplicates from (%s) with intermediate directory (%s).\n' % (src, dst))
    else:
        stdout.write('[main] INFO: Removing duplicates from (%s) and storing in (%s).\n' % (src, dst))
    
    # Get the hash of all files and their paths
    hashes = compute_file_hashes(src, recurse=True)
    stdout.write('[main] INFO: Computed (%d) unique hashes.\n' % (len(hashes)))
    
    # Iterate the hashes, saving the files into the destination
    for hash in hashes:
        file = hashes[hash].replace(src, dst)
        tree = file.split(os.sep)
        if(rename):
            old_name = tree[-1]
            ext = old_name.split('.')[-1]
            file = file.replace(old_name, (hash + '.' + ext))
        sub = os.sep.join(tree[:-1])
        if(not os.path.isdir(sub)):
            stdout.write('[main] INFO: Creating sub directory (%s).\n' % (sub))
            os.makedirs(sub)
        if(move):
            stdout.write('[main] INFO: Moving (%s) to (%s).\n' % (hashes[hash], file))
            shutil.move(hashes[hash], file)
        else:
            stdout.write('[main] INFO: Copying (%s) to (%s).\n' % (hashes[hash], file))
            shutil.copyfile(hashes[hash], file)
    
    # If no destination was specified, replace the source with the tmp destination
    if(is_tmp):
        shutil.rmtree(src)
        shutil.move(dst, src)


"""
Entrypoint
"""
if __name__ == '__main__':
    stdout.write('\n')
    if(len(argv) < 5):
        stdout.write('USAGE: %s <src_dir> <dst_dir> <rename> <do_not_copy>\n' % (argv[0]))
    else:
        if(not os.path.isdir(argv[1])):
            stdout.write('Not a directory (%s).\n' % (argv[1]))
        else:
            if(not os.path.isdir(argv[2])):
                os.mkdir(argv[2])
            argv[3] = argv[3].lower()[0]
            argv[4] = argv[4].lower()[0]
            main(argv[1], argv[2], (argv[3] == 't' or argv[3] == 'y'), (argv[4] == 't' or argv[4] == 'y'))
    stdout.write('\n')
