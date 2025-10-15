TERMS 

- Phoneme
    - the unit of speech, IE a single sound you can make speaking. These vary per langauage
- Graphene
    - the text equivalent of a Phoneme, like a syllable. 
- The CMU Pronouncing DIctionary    
    - Database of graphenes 
- Vocoder
    - transforms 
- Autoregressive: predicts using prior predictions, like LLM contexts
- Prosody: pertaining to prose, referring to intonation, stress, and rythm
- Pinyin: romanization library for chinese characters
- Mel scale: analagous scale to the frequency of sound waves, but adjusted to be linear to human perception.
- Spectrogram: graph of sound data. X is time, Y is amplitude, Z (or color) is intensity. 
- Mel Spectrogram: spectrogram with mel scale instead of freqneucy, so akin to a human audible spectrogram. 


- Flow Matching
- Classifier-free guidance


# FURTHER READING 
- diffusion transformers (DiT) from meta
- ConvNeXt V2
- Enhanced transformer with rotary position embedding
- U-net: segmentation model 
- aLiBi: Attention with linear biases. TLDR bias against old tokens, linearly, for improved context use



F5-TTS: PAPER
- The problem with autoregressive speech models: error accumulation (or "exposure bias") and serial inference
    - This is why lots of voice cloning models can work with short input secuenses - just a few seconds - that's functioning as a prompt to be continued. neat! 
- The solution: direct modeling in continuous space
- Diffusion seems like a promising approach for speech problems. Flow matching with optimal transport path
- NAR models are very dependent on good tokenizers. They can also make speech sound less natural, since phenomes should context to eachother to get things like intonation right.
- Novel controbutions with F5: removed phoneme alignment, duration predictor, text encoder, and semantically infused codec model. Works entireley off of a diffusion transformer and ConvNeXt V2 (CNN)

- note: come back to section 2 "preliminaries" 

- 3: Method
    - 3.1: Training
        - "Infilling task" - similar to how tokens are masked during training of an llm. 



# RoFormer: Enhanced Transformer with Rotary Position Embedding 
https://arxiv.org/abs/2104.09864


