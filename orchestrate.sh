#!/bin/sh

# when restarting:

# git commit all
# git push origin master
python setup.py install
cd /opt/dig/venv/dig
rm ../dig.zip
zip -r ../dig.zip *
hadoop fs -rm /user/philpot/hs/archive/dig.zip
hadoop fs -put /opt/dig/venv/dig.zip /user/philpot/hs/archive

cd $PROJ/dig-extract
hadoop fs -rm /user/philpot/hs/file/backpage.py
hadoop fs -put dig/extract/page/backpage.py /user/philpot/hs/file

hadoop fs -rm /user/philpot/hs/file/phone.py
hadoop fs -put dig/extract/entity/telephone/phone.py /user/philpot/hs/file

hadoop fs -rm /user/philpot/hs/file/digtoken.py
hadoop fs -put dig/extract/entity/digtoken/digtoken.py /user/philpot/hs/file

hadoop fs -rm /user/philpot/hs/file/workingname.py
hadoop fs -put dig/extract/entity/workingname/workingname.py /user/philpot/hs/file

hadoop fs -rm /user/philpot/hs/file/patscan.py
hadoop fs -put dig/extract/entity/classifier/patscan.py /user/philpot/hs/file