import os
import shutil
from tempfile import TemporaryDirectory
from hashlib import md5
from sys import stdout, argv


EXTS = ['jpg', 'png', 'gif', 'jpeg',
        'mp4', 'm4v', 'mkv', 'webm',
        'mp3', 'wav']


"""
Driver function. Save only unique files from a source directory into a destination directory.
@param src - Source to query.
@param dst - Destination free of duplicates. If None, use a tmp directory and overwrite the source.
"""
def main(src, dst):
    # If no destination was specified, take note and create a tmp directory
    is_tmp = False
    if(dst is None):
        is_tmp = True
        dst = TemporaryDirectory().name
        os.mkdir(dst)
    stdout.write('Removing duplicates from (%s) and storing in (%s).\n' % (src, dst))
    
    
    
    # If no destination was specified, replace the source with the tmp destination
    if(is_tmp):
        shutil.rmtree(src)
        shutil.move(dst, src)


"""
Entrypoint
"""
if __name__ == '__main__':
    stdout.write('\n')
    if(len(argv) < 2):
        stdout.write('USAGE: %s <src_dir> ?dst_dir?\n' % (argv[0]))
    else:
        if(not os.path.isdir(argv[1])):
            stdout.write('Not a directory (%s).\n' % (argv[1]))
        else:
            if(len(argv) < 3):
                argv.append(None)
            elif(not os.path.isdir(argv[2])):
                os.mkdir(argv[2])
            main(argv[1], argv[2])
    stdout.write('\n')
