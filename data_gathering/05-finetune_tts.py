import os
import json
from TTS.trainer import Trainer, TrainingArgs
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.datasets import load_tts_samples
from TTS.tts.models.vits import Vits
from TTS.utils.audio import AudioProcessor

def finetune_tts(dataset_file, output_path):
    # Load the dataset
    with open(dataset_file, 'r') as f:
        metadata = json.load(f)

    # Prepare the dataset
    dataset = load_tts_samples(metadata)

    # Configure the model
    config = VitsConfig()
    config.audio.sample_rate = 22050  # Adjust if your audio has a different sample rate
    config.batch_size = 32
    config.eval_batch_size = 16
    config.num_loader_workers = 4
    config.num_eval_loader_workers = 4
    config.run_eval = True
    config.test_delay_epochs = -1
    config.epochs = 1000
    config.text_cleaner = "english_cleaners"
    config.use_phonemes = True
    config.phoneme_language = "en-us"
    config.output_path = output_path

    # Init audio processor
    ap = AudioProcessor.init_from_config(config)

    # Init the model
    model = Vits(config, ap)

    # Init the trainer
    trainer = Trainer(
        TrainingArgs(),
        config,
        output_path,
        model=model,
        train_samples=dataset,
        eval_samples=dataset[:100],
    )

    # Start training
    trainer.fit()
    
    # save the model
    trainer.save_model()

if __name__ == "__main__":
    dataset_file = 'tts_dataset.json'
    output_path = 'tts_output'
    finetune_tts(dataset_file, output_path)
