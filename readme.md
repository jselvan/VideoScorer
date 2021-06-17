# VideoScorer
VideoScorer is a custom tk gui that allows customizable scoring of videos  
VideoScorer assumes the directory contains a behaviour.csv file with indices corresponding to separate video files.  
Use `Configure>File Template` to tell VideoScorer how your videos are named.

Requires VLC to be installed and the following python packages:

* numpy
* pandas
* python-vlc
* click

Install using:
```powershell
pip install git+https://github.com/jselvan/VideoScorer.git
```