username=$1
server=$2
remote_path=$3
local_alias=$4
scp -r $username@$server:$remote_path ./tmp
rm -rf $local_alias
mv tmp $local_alias
rm -rf tmp