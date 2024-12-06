# read2me
generate audiobooks with epubs and cloned voices

Motivated to start this project after finding out that cancelling my audble subscription means I lost all the books I already bought. fuck that. 

# TODO

- input epubs -> extract chapters
- use off the shelf text to speech API 
- output a dir of .mp3s of narrated voice

Step 2, what would be way cooler: clone a voice
- input audio / video of a voice (someone giving a speech, for example)
  - generate text from audio (whisper API)
  - generate voice from text + audio
- input epub
  - generate chapters
- output narrated chapter mp3s


# BUGS

- all books have uniue structures to chapter headers - some manual cleaning is needed




# USAGE STEPS
- get name/clip pair and load into voice_clips.json
- run through data_gathering dir to generate dataset
- finetuning/finetune.sh
  - adjust hyperparams in tacotron.py
  - run tensorboard.sh to watch training
- test_model.sh to get outputs 

