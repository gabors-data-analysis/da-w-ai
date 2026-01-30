#!/usr/bin/env python3
# ----------------------------------------------------------------------------------------------------------------------
# Script: classify_manager_sentiment.py
# Description: Loads post-match manager quotes and rates overall sentiment using OpenAI's GPT API.
#              Applies explicit guidelines to assign a score from -2 to 2 for each statement.
# ----------------------------------------------------------------------------------------------------------------------

import os
import sys
import time
import json
import logging
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from tqdm import tqdm

# ----------------------------------------
# Configure logging
# ----------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('classification.log', mode='w')
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# ----------------------------------------
# Initialize the OpenAI client (API key)
# ----------------------------------------
# Directly assign your API key here; ensure it remains confidential
api_key = os.getenv("OPENAI_API_KEY")  # It's more secure to load from environment
if not api_key:
    logger.error('OPENAI_API_KEY not set in environment')
    sys.exit(1)
client = OpenAI(api_key=api_key)
logger.info('OpenAI client initialized')

# ----------------------------------------
# Define input CSV path
# ----------------------------------------
POST_MATCH_CSV = "data/post_match_texts.csv"
FILE_ENCODING = 'windows-1252'

# ----------------------------------------
# Load data
# ----------------------------------------
def load_csv(path, encoding=None, **kwargs):
    try:
        df = pd.read_csv(path, encoding=encoding, **kwargs)
        logger.info(f"Loaded {len(df)} rows from {path}")
        return df
    except Exception as e:
        logger.error(f"Failed to load {path}: {e}")
        sys.exit(1)

posts_df = load_csv(POST_MATCH_CSV, encoding=FILE_ENCODING, on_bad_lines='skip')

# Validate required columns
required_cols = {'text_id', 'game_id', 'manager_id', 'processed_tex'}
missing = required_cols - set(posts_df.columns)
if missing:
    logger.error(f"Missing columns in CSV: {missing}")
    sys.exit(1)

# ----------------------------------------
# Classification function
# ----------------------------------------
# Use model 'gpt-4.1-2025-04-14' in the future can change to any different model

def classify_text(text, model='gpt-4.1-2025-04-14', retries=3):
    """
    Uses GPT to rate sentiment from -2 (strong negative) to +2 (strong positive).
    Returns integer score or None on failure.
    """
    guidelines = '''## Task:

Please read each text carefully and rate the overall sentiment of the manager's statement as positive or negative.
Your rating should reflect the manager’s expressed tone, not your judgment of the match.

## Rating Scale:

| **Score** | **Meaning** |
|----------|------------|
| **2** | Strongly positive sentiment (clear optimism, satisfaction, praise). |
| **1** | Mildly positive sentiment (generally positive, slight reservations). |
| **0** | Neutral or unclear sentiment. |
| **-1** | Mildly negative sentiment (general disappointment, frustration). |
| **-2** | Strongly negative sentiment (clear criticism, significant disappointment). |

### Final Notes:
- Use **0** if unsure or if sentiment is mixed without clear dominance.
'''
    prompt = f"""{guidelines}
Now rate this manager statement:

"""{text}"""

Reply with only the integer score (e.g., 2 or -1)."""

    for attempt in range(1, retries+1):
        try:
            logger.info(f"API attempt {attempt}, prompt length={len(prompt)} chars")
            resp = client.chat.completions.create(
                model=model,
                messages=[{'role':'user','content':prompt}],
                temperature=0
            )
            out = resp.choices[0].message.content.strip()
            logger.info(f"[API] output: {out}")
            score = int(out)
            return score
        except ValueError:
            logger.error(f"Could not parse integer from response: {out}")
            return None
        except Exception as e:
            logger.error(f"API error on attempt {attempt}: {e}")
            if attempt == retries:
                logger.error("All API attempts failed; returning None")
                return None
            time.sleep(2**(attempt-1))
    return None

# ----------------------------------------
# Process all quotes
# ----------------------------------------
results = []
for _, row in tqdm(posts_df.iterrows(), total=len(posts_df), desc='Classifying'):
    score = classify_text(row['processed_tex'])
    results.append({
        'text_id': row['text_id'],
        'game_id': row['game_id'],
        'manager_id': row['manager_id'],
        'score': score
    })

results_df = pd.DataFrame(results)

# ----------------------------------------
# Save results
# ----------------------------------------
output_file = 'manager_sentiment_results.csv'
results_df.to_csv(output_file, index=False)
logger.info(f"Saved {len(results_df)} records to {output_file}")
logger.info("Score distribution:\n" + results_df['score'].value_counts(dropna=False).to_string())
