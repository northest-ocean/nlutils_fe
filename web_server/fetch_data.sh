server=$1
scp -r xchen648@$server.cc.gatech.edu:/nethome/xchen648/mliu444_codes/HybridModel/experiments/params ./tmp
rm -rf $server
mv tmp $server