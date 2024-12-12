from celery import Celery
import os

# Initialize Celery with Redis as broker
celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task(bind=True)
def clone_voice(self, name, source_filename, input_text):
    source_wav = os.path.join("data/audio", name, "wavs", f"{source_filename}.wav")
    output_path = f"output/{self.request.id}.wav"
    
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Run the cloning script
    os.system(f"python3 endpoints/simple-clone.py {source_wav} {input_text} {self.request.id}")
    
    return {
        'task_id': self.request.id,
        'status': 'completed',
        'output_path': output_path
    }
