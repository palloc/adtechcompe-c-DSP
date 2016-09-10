yum install -y epel-release
yum install -y python-devel
yum install -y python-pip
yum install -y gcc gcc-c++ openssl-devel
yes | pip install pandas
yes | pip install tornado aerospike
yes | pip install --upgrade pip
yes | pip install scipy
yes | pip install sklearn
