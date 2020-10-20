# installation

``
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh ~/
chmod +x ~/Miniconda3*.sh
~/Miniconda3*.sh

sudo yum install git 
git clone https://github.com/JustinGuese/autoscout24-crawler ~/autoscout24-crawler
cd ~/autoscout24-crawler
conda create --name autoscout 
source activate autoscout
conda install pip
pip install -r requirements.txt
``

# multiprocessing

sometimes single are faster. try running multiprocess

`python autoscouter.py`

## no multiprocess

## run scheduler via python

`python dfMergerCronNotWorking.py`

## run crawler (no multiprocess)

`python autoscouter_nomultiprocess.py`

e.g. run every command in one screen session or so
