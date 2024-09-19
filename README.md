<div align="center">
  
# CtrlSpeak
  
<p align="center">
  <img src="https://img.shields.io/badge/license-Please%20Don't%20Use%20This%20For%20Evil!-red.svg" alt="License">
  <a href="https://w404.net/">
    <img src="https://img.shields.io/badge/by-W404.NET-purple.svg" alt="W404.NET">
  </a>
</p>

</div>

<p align="center">
  <img width="30%" src="https://github.com/user-attachments/assets/9a837419-6636-4d39-b865-53ecf39eb742" alt="Logo CtrlSpeak">
</p>

## Introduction

I was getting bored with chatbots that constantly speak without being prompted and answer when I don't ask. So, I decided to create **CtrlSpeak**, a voice assistant that listens and responds only when you want it to.

This project utilizes **Groq** to convert speech to text, allows you to use any AI model for chat responses, and converts the AI's text response back to speech using **Deepgram**. Note that Deepgram offers a free $200 credit upon first signup.

## Features

- **On-Demand Listening**: The assistant starts listening when you press **[Control] + Q** by default.
- **Speech-to-Text Conversion**: Use Groq to transcribe spoken words into text.
- **AI Model Integration**: Integrate any AI model (e.g., GPT-3, GPT-4) to generate chat responses.
- **Text-to-Speech Conversion**: Convert text responses back to speech using Deepgram.

## Getting Started

### Prerequisites

- **Groq Account**: Sign up for a Groq account and obtain an API key for speech-to-text conversion.
- **Deepgram Account**: Sign up for a Deepgram account to get your API key (free $200 credit on first signup).
- **AI Model/API**: Access to an AI model or API (e.g., OpenAI API key for GPT models).

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/MinhxThanh/ctrlspeak.git
   cd ctrlspeak
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**

   Change `.env.example` to `.env` and add your API keys:

### Usage

Run the main application:

```bash
python main.py
```

Press **[Control] + Q** to start the assistant. Speak into your microphone, and the assistant will listen, process your query, and respond with synthesized speech.

## What Next?

We're excited to announce upcoming features that will enhance your experience with CtrlSpeak:

### Copy Ask

**How it works:** When you copy text from any application (like a document, webpage, or email), you can invoke CtrlSpeak to interact with the copied content. Simply press a designated keyboard shortcut (e.g., **[Control] + C + A**) and ask the assistant what you can do with the copied text.

**Examples:**

- "Summarize the copied text."
- "Translate the copied text to French."
- "Create a brief email response based on this text."

This feature allows you to quickly process and manipulate text without leaving your current application.

### Screen Ask

**How it works:** Press a keyboard shortcut (e.g., **[Control] + Shift + S**) to capture a screenshot of your current screen. CtrlSpeak will process the image, and you can ask questions about what's displayed.

**Examples:**

- "What is on my screen right now?"
- "Read any error messages on the screen."
- "Identify any actionable items in this image."

By integrating OCR (Optical Character Recognition) and image recognition technologies, this feature helps you interact with visual information seamlessly.

---

*Stay tuned for these exciting new features! Your feedback and contributions are highly appreciated.*

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the **"Please Don't Use This For Evil!"** license.

## Acknowledgements

- **Groq** for speech-to-text services.
- **Deepgram** for text-to-speech services.
- **OpenAI** for AI model inspiration.

## Contact

For questions or suggestions, please open an issue or contact me directly at [minhthanh@onename.net](mailto:minhthanh@onename.net).

---
