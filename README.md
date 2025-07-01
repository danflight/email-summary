# email-summary

A simple Python tool to fetch your 20 most recent Gmail messages and summarise them using NLP models.

## Features

- Authenticates securely with your Gmail account (OAuth2)
- Fetches sender, subject, date, and snippet/body of recent emails
- Prints your emails in a clear, vertical list
- Summarises email content using Hugging Face transformers (BART), ChatGPT (OpenAI) or TextRank (sumy)
- Optionally emails the summary to yourself using the Gmail API

## Setup

1. **Clone the repository and install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Get Gmail API credentials:**
    - Go to [Google Cloud Console](https://console.cloud.google.com/).
    - Create a project, enable the Gmail API, and configure the OAuth consent screen.
    - Create OAuth client credentials (Desktop app) and download `credentials.json`.
    - Place `credentials.json` in your project root.


## Usage

Run the main script:
```bash
python src/main.py
```
- The first run will prompt you to log in and authorize access to your Gmail.
- The script will print your 20 most recent emails in a vertical list.
- It will also print a summary of those emails.
- The summary will be emailed to you automatically.

## Troubleshooting

- **403 Error / API not enabled:**  
  Enable the Gmail API for your Google Cloud project.

- **OAuth consent error:**  
  Add your email as a test user in the OAuth consent screen.

- **Model loading error:**  
  Install PyTorch or TensorFlow as described above.

## Customisation

- To change the number of emails fetched, edit the `fetch_recent_emails` call in `src/main.py`.
- To use extractive summarisation, change the method to `'textrank'` in `summarize_emails_snippets`.
- To change the recipient of the summary email, edit the `to_email` argument in `send_email_via_gmail` in `src/main.py`.

## License

MIT