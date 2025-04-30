# Kinyarwanda Audio Q&A System

A speech-to-text question answering system that:
- Transcribes audio questions in kinyarwanda using KinyaWhisper model
- Matches against a knowledge base
- Returns accurate answers

## Features
- **Kinyarwanda language support**
- **Audio processing** 
- **Fuzzy matching** 
- **Fast response** 

## Installation

1. Clone the repository:
```bash
git clone https://github.com/christejab07/Kinya-assistant.git
cd Kinya-assistant
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage
1. Prepare Your Q&A Database

Edit `qa.json`

```bash
{
	"mwiriwe": "mwiriweho",
	"umezeneza": "mezeneza",
	"muraho": "murahoneza",
	"amakuruyawe": "nimeza",
	"ukoriki": "ndiga"
}
```

2. Run the System
```bash
python get_res.py --input path/to/your_audio.wav
```

3. Example Output
``` bash
Recognized Question: umezeneza
Best Match: umezeneza
Answer: mezeneza
```