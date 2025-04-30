import json
import torch
import torchaudio
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# 1. Load Q&A database
qa_db = {
	"mwiriwe": "mwiriweho",
	"umezeneza": "mezeneza",
	"muraho": "murahoneza",
	"amakuruyawe": "nimeza",
	"ukoriki": "ndiga"
}

# Save to JSON (for demo)
with open("qa.json", "w") as f:
    json.dump(qa_db, f)

# 2. Load Whisper model
processor = WhisperProcessor.from_pretrained("benax-rw/KinyaWhisper")
model = WhisperForConditionalGeneration.from_pretrained("benax-rw/KinyaWhisper")

def transcribe_audio(audio_path):
    """Convert speech to text using Whisper with proper attention handling"""
    try:
        # Load and preprocess audio
        waveform, sample_rate = torchaudio.load(audio_path)
        if waveform.dim() > 1 and waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0)
        
        # Process with Whisper
        inputs = processor(
            waveform.numpy(),
            sampling_rate=sample_rate,
            return_tensors="pt",
            padding=True  # Enable automatic padding handling
        )
        
        # Generate with proper attention handling
        with torch.no_grad():
            predicted_ids = model.generate(
                input_features=inputs.input_features,
                max_new_tokens=128
            )
        
        return processor.batch_decode(predicted_ids, skip_special_tokens=True)[0].lower().strip()
    
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return None

def find_best_match(question, db):
    """Find closest matching question using fuzzy matching"""
    try:
        # Normalize the input question
        normalized_question = question.lower().strip()
        
        # Find best match with score threshold
        best_match, score = process.extractOne(
            normalized_question,
            db.keys(),
            scorer=process.fuzz.token_sort_ratio
        )
        
        return db[best_match] if score > 65 else "I didn't understand that question"
    except:
        return "Sorry, I couldn't find an answer"

def qa_pipeline(audio_file):
    """Complete Q&A processing pipeline"""
    # Step 1: Transcribe audio
    question = transcribe_audio(audio_file)
    if not question:
        return "Could not transcribe the audio"
    
    print(f"\nRecognized Question: {question}")
    
    # Step 2: Find matching answer
    answer = find_best_match(question, qa_db)
    return answer

# Example usage
if __name__ == "__main__":
    # Test with an audio file (replace with your actual file)
    result = qa_pipeline("rw-test01.wav")
    print("\nFinal Answer:", result)
