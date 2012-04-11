import urllib2
import os
import gzip

root_url = 'ftp://ftp.ncdc.noaa.gov/pub/data/noaa/'

def get_data_dirs():
    lst = urllib2.urlopen(root_url).readlines()
    flst = []
    for l in lst:
        elm = l.split()
        ftype = elm[0]
        is_dir = ftype.startswith('d')
        if is_dir:
            try:
                dname = elm[-1].strip()
                int(dname)
                flst.append(dname)
            except:
                pass
    return flst

def list_data_files(remote_dir):
    lst = urllib2.urlopen(remote_dir).readlines()
    flst = []
    for l in lst:
        elm = l.split()
        fname = elm[-1].strip()
        if fname.endswith('.gz'):
            flst.append(fname)
    return flst

def get_data_file(remote_dir, remote_file, local_dir='.', local_file=None):
    if not remote_dir.endswith('/'):
        remote_dir += '/'
    url = remote_dir + remote_file
    gz = urllib2.urlopen(url)
    if local_file is None:
        local_file = remote_file
    if not local_dir.endswith('/'):
        local_dir += '/'
    local_path = local_dir + local_file
    open(local_path, 'wb').write(gz.read())

def get_directory(data_dir, local_dir):
    data_dir = root_url + data_dir + '/'
    for fname in list_data_files(data_dir):
        try:
            get_data_file(data_dir, fname, local_dir)
        except Exception, inst:
            print 'Failed to download %s ' % fname
            print 'Retrying'
            try:
                get_data_file(data_dir, fname, local_dir)
            except Exception, inst:
                print 'Retry failed'

def get_all_data(local_root, startwith='1901'):
    if not local_root.endswith('/'):
        local_root += '/'
    for d in get_data_dirs():
        if startwith is None or d > startwith:
            local_dir = local_root + d
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            get_directory(d, local_dir)

