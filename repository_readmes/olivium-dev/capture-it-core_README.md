# README for olivium-dev/capture-it-core


# Capture-It-Core

## Overview

Capture-It-Core is a powerful and efficient tool designed to extract and transcribe audio from social media videos. By simply inputting a video URL from popular social media platforms, users can quickly generate accurate transcripts, making this tool ideal for content creators, researchers, and social media enthusiasts who need to convert video content into written form.

## Features

-   **Video Downloading**: Supports downloading videos from various social media platforms.
-   **Audio Extraction**: Efficiently extracts audio from downloaded videos.
-   **Transcription**: Utilizes advanced AI to transcribe the extracted audio into text.
-   **Ease of Use**: Simple and intuitive interface, requiring only a video URL to operate.

## Installation

To set up Capture-It-Core on your system, follow these steps:

1.  **Clone the Repository**
    
    bashCopy code
    
    `git clone https://github.com/your-username/capture-it-core.git
    cd capture-it-core` 
    
2.  **Install Dependencies** Install all the necessary Python packages by executing the following commands:
    
    bashCopy code
    
    `pip install pydub
    pip install moviepy
    pip install pytube
    pip install flask
    pip install slack-sdk
    pip install torch
    pip install whisper` 
    

## Usage

To use Capture-It-Core, follow these simple steps:

1.  **Start the Application** Run the application using:
    
    bashCopy code
    
    `python app.py` 
    
2.  **Enter Video URL** Input the URL of the social media video you wish to transcribe.
    
3.  **Transcription** The tool will download the video, extract the audio, and transcribe the content. The transcript will be displayed or saved as per the configured settings.
    

## Configuration

-   The configuration file (`config.json`) can be edited to change default settings like download paths, output formats, etc.

## Contributing

Contributions to Capture-It-Core are welcome. Please ensure to follow the coding standards and guidelines provided in the `CONTRIBUTING.md` file.

## License

Capture-It-Core is released under the [MIT License](https://chat.openai.com/c/LICENSE).

## Support

For support, you can open an issue in the GitHub repository, or contact the maintainers directly via email.

## Acknowledgments

A special thanks to the open-source libraries and APIs that made this project possible.