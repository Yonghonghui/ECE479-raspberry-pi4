# raspberry-pi4
final demo: smart assistant based on chat-gpt on pi4


https://github.com/haoyuh3/raspberry-pi4/assets/148392769/0036d5a8-acd3-4428-bbf9-b62fb8b40f42


you can config your raspberry pi according to lab2

##tensorflow
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install libhdf5-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test
wget https://raw.githubusercontent.com/jasondeglint/tf/main/install_tensorflow.sh
source install_tensorflow.sh

Afterward, you can test the installation with

python3 -c "import tensorflow as tf;print(tf.reduce_sum(tf.random.normal([1000, 1000])))" 
And check the installation of Keras through
from tensorflow import keras

##face recognition/ text-speech/ speech-text/ google cloud/ openai
pip install gtts
pip install pygame
pip install openai
pip install google-cloud-storage
pip install SpeechRecognition
pip install pyaudio
sudo apt-get install python-pyaudio python3-pyaudio
sudo apt-get install flac

numpy down grade!!!!!!!!!!
Uninstall numpy

Install face_recognition

