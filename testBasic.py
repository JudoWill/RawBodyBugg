import nose.tools
from subprocess import check_call
import shlex
import csv
import os.path, os

def test_basic_call():

    if os.path.exists('nfile.csv'):
        os.remove('nfile.csv')
    
    cmd = shlex.split('python bmhack.py --fromDump=ftest.cpickle --toCsv=nfile.csv')
    check_call(cmd)    

    assert os.path.exists('nfile.csv'), 'Did not create file!'

    with open('nfile.csv') as handle:
        with open('ftest.csv') as rhandle:
            treader = csv.DictReader(handle, delimiter = '\t')
            creader = csv.DictReader(rhandle, delimiter = '\t')
            for ind, (cor, tes) in enumerate(zip(creader, treader)):
                assert cor == tes, str(cor) + str(tes) + str(ind)


