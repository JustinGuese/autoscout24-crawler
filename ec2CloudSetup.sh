#!/bin/bash
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