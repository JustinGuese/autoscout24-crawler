#!/bin/bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh ~/
chmod ~/Miniconda3*.sh
~/Miniconda3*.sh

sudo yum install git 
git clone https://github.com/JustinGuese/autoscout24-crawler ~/autoscout24-crawler
cd ~/autoscout24-crawler
conda env create -f environment.yml
source activate autoscout

