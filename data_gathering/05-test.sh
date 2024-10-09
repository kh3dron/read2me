latest_run="run-October-08-2024_05+29PM-a79e346"

tts --text "Checking in on the state of the last training run. The quick brown fox jumps over the lazy dog." \
      --model_path $latest_run/best_model.pth \
      --config_path $latest_run/config.json \
      --out_path $latest_run/test.wav