import nose.tools
from subprocess import check_call
from itertools import izip_longest
import shlex
import csv
import os.path, os

import bmhack

def check_equal_files(cfile, tfile):
    """Tests to check whether two CSV files are equivelent."""
    
    with open(tfile) as thandle:
        with open(cfile) as chandle:
            treader = csv.DictReader(thandle, delimiter = '\t')
            creader = csv.DictReader(chandle, delimiter = '\t')
            for ind, (cor, tes) in enumerate(izip_longest(creader, treader)):
                if cor is None or tes is None:
                    assert False, 'Files are not the same length!'
                tes.pop(None, None)
                assert cor == tes, str(cor) + str(tes) + str(ind)


def test_basic_call():

    if os.path.exists('nfile.csv'):
        os.remove('nfile.csv')
    
    cmd = shlex.split('python bmhack.py --fromDump=ftest.cpickle --toCsv=nfile.csv')
    check_call(cmd)    

    assert os.path.exists('nfile.csv'), 'Did not create file!'

    check_equal_files('nfile.csv', 'ftest.csv')
    
def test_main_call_csv_only():
    
    tfile = 'nfile.csv'
    if os.path.exists(tfile):
        os.remove(tfile)
        
    bmhack.main('ftest.cpickle', False, False, tfile, None)
    assert os.path.exists(tfile), 'Did not create file!'

    check_equal_files(tfile, 'ftest.csv')
    
def test_double_call():

    cmd = shlex.split('python bmhack.py --fromDump=ftest.cpickle --fromSerial=COM1 --toCsv=nfile.csv')

    try:
        check_call(cmd)
        assert True, 'Should have raised error!'
    except:
        pass
