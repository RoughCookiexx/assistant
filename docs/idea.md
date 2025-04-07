```mermaid
flowchart TD
A[Android App: Record voice] --> B[Save temp file]
B --> C[Upload to S3 bucket]
C --> D[API Request: Filename]

D --> E[API Thread: Response OK/FUCK to client]
E --> F[Download from S3]
F --> G[Transcribe audio with Whisper]

G --> H[Send text to ChatGPT]
H --> I[Match Intent via YAML config]

I --> J{Is it a device command?}
J -- Yes --> K[Send response + function + params to Android]
J -- No --> L[Send 'Working on it' message to Android]
L --> M[Execute command on server]
M --> N[Send "Done" message + details to Android]
