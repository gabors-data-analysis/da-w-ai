# Week 07: using text as data

## Overview

In this lesson, students will be introduced to sentiment analysis, specifically applied to evaluating general positivity or negativity in football managers' statements about match outcomes.

### Learning Outcomes

By the end of the session, students will:
- Gain hands-on experience with sentiment analysis.
- Understand the complexities and limitations of sentiment analysis.

### Materials

- General Sentiment (positive/negative) rating scale [HERE](/week07/assets/sentiment-scale.md)
- CSV files:
  - `student_test_5` download from [HERE as xlsx](/week07/assets/student_test_5.xlsx) [HERE as csv](/week07/assets/student_test_5.csv), (or from moodle)


## Assignment review

* Fancy graphs != good graphs (good graph <- careful design)
* Precise interpretation >> BS
* Less is more
* Show only what you understand deeply 

## Lecture: NLP basics

- **Topic:** Introduction to Sentiment Analysis
- **Key points:**
  - Importance of text analysis and its applications 
  - Introduction to Natural Language Processing (NLP): definition and applications 
  - Key concepts in text analysis:
    - Tokenization 
    - Preprocessing techniques
    - Feature extraction 
  - Sentiment analysis: detecting emotion and tone in text
  - Practical examples from football managers' post-match interviews
  - Limitations and challenges in text analysis, emphasizing contextual interpretation and ambiguity

[Slides](https://gabors-data-analysis.com/courses/da-w-ai-2025/da-w-ai-05-text-to-data#/title-slide)

**domain lexicons**
* [simple version](/data/interviews/domain_lexicon.csv)
* [better created by AI](/code/interviews/domain_lexicon.R)

## Practical Activity

### Manual vs AI Sentiment Analysis Activity

- **Objective:** Practice manually rating football manager statements as positive or negative.
- **Steps:**
  1. Review general sentiment rating scale provided [HERE](/week07/assets/sentiment-scale.md)
  2. Individually analyze and rate **5 provided test statements** from `student_test.csv`.
  3. Now use AI to rate them.
  4. Try have a better domain lexicon. 
 
Discuss experience, how AI helps, what could go wrong. 

### Prediction of score

* Modeling choices of results
* Think about *how* you would do it first
* Check how AI thinks about, rate the examples and look at explanations
* take the 5 examples, and compare your predictions vs the AI predictions  

### Discussion: Validation and Sentiment Analysis

- **Objective:** Discuss validation techniques used in sentiment analysis.
- **Topics for discussion:**
  - Differences between manual and AI ratings
  - Ground Truth
  - Introduction to validation methods:
  - If ground truth -- can do confusion maztric, calculate accuracy
  - If no ground truth -- measure **agreement** between humans and AI. test difference.
    - AI is average, but... 
    - AI with persona?
    - AI biased ?   
    
## End of Week Discussion points

* How precise is AI in sentiment analysis?
* How did *you* compare to AI in terms of scores? How did any difference make you feel? 
* Can you think of a past project where AI could have helped you upgrade it?
