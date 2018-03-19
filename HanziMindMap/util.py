import subprocess


def speak(word):
    subprocess.call(['say', '-v', 'ting-ting', word])
