sudo apt install virtualenv

virtualenv --version

cd ~

mkdir kafka_lab3
cd kafka_lab3

virtualenv -p /usr/bin/python3 crypto

source crypto/bin/activate

python --version

pip install kafka-python
pip install gcloud
pip install google-cloud-storage
pip install google-api-python-client
