### Filesystem structure
anything with a 1 can have many objects at that level

data/
    audio/
        speakername/
            sources.json
            source1/
                transcript.txt
                source1.wav
                clips/
                    transcripts.json
                    clip1.wav
    text/
        user_edited/
            user1.json
        source1/
            source.epub
            source.txt
            chapters/
                chapter1.txt
    generations/
        id.wav
    models/
        phenome_cache/
        model1/
            model.pth
            script.py
    metadata/
        builtin_model_data.json

# JSON schemas
data/audio/speakername/sources.json
[
    [sourcename: youtube_url]
]

data/audio/speakername/source1/clips/transcripts.json
[
    [clipname: transcript]
]

data/text/user_entered/user1.json:
[
    [taskid: text]
]

# Types of voices
- use a built in voice from a model 
    - key from builtin voices db
- use a model to clone with an input .mp3 file
    - foreign key of models db 
    - file path 
- use a custom voice
    - path to training script 


# Postgres Schema
- users
    - username
    - email 
    - time_created
    - password
    - generation_limit
- models (builtin to tts)
    - model_name
- builtin voices
    - model (foreign to models db)
    - voice_name (text)
    - sex (bool nullable)
    - notes (global user editable text) #todo break out to per user later
- generations
    - input text file (nullable)
    - input text task ID
    - voice type (one of: clone, generic, custom)
    - voice input (nullable)
    - voice name (nullable)
    - voice model_file (nullable)
    - datetime
    - owner
    - output audio file 
    - constrains:
        - must have text file OR raw text fields
        - if voice type 
            - clone: must have voice input
            - generic: must have voice name (builtin voice foreign key)
            - custom: must have voice model_file

- custom voices
    - input training script (which stores all other hyperparams)
    - output model file (.pth)
