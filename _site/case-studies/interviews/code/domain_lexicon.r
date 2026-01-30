# Create a domain-specific lexicon for football manager interviews
# This script generates a CSV file containing football-specific terms and their sentiment values

# Create a dataframe for the domain lexicon
domain_lexicon <- data.frame(
  word = character(),
  sentiment_score = numeric(),
  stringsAsFactors = FALSE
)

# Add positive football terms with sentiment scores
positive_terms <- data.frame(
  word = c(
    # Performance-related positive terms
    "win", "victory", "winning", "won", "beat", "defeated", "success", "successful",
    "outstanding", "brilliant", "excellent", "exceptional", "fantastic", "perfect", "superb",
    "great", "quality", "class", "solid", "dominant", "dominance", "control", "controlled",
    "strong", "strength", "powerful", "dominate", "dominated", "consistent", "consistency",
    
    # Improvement-related positive terms
    "improve", "improved", "improvement", "progress", "developing", "development", "grow", "growing",
    "potential", "promising", "talent", "talented", "prospect", "build", "building",
    
    # Team dynamics positive terms
    "team", "teamwork", "together", "spirit", "character", "attitude", "committed", "commitment",
    "hard-working", "effort", "determined", "determination", "fight", "fought", "resilient", "resilience",
    
    # Emotion-related positive terms
    "happy", "pleased", "delighted", "proud", "satisfied", "enjoy", "enjoyed", "confidence", "confident",
    "positive", "optimistic", "optimism", "excited", "exciting", "believe", "believing", "faith",
    
    # Achievement-related positive terms
    "goal", "goals", "score", "scored", "scoring", "assist", "assists", "clean sheet", "clean",
    "chance", "chances", "opportunity", "opportunities", "create", "created", "creating",
    "deserve", "deserved", "reward", "rewarded", "earn", "earned",
    
    # Game management positive terms
    "tactics", "tactical", "strategy", "plan", "prepared", "preparation", "disciplined", "discipline",
    "organized", "organization", "professional", "managed", "control", "adapt", "adapted", "flexibility"
  ),
  sentiment_score = c(
    # Performance scores (1.5-2.0)
    1.9, 1.9, 1.8, 1.8, 1.7, 1.7, 1.8, 1.8,
    1.9, 1.8, 1.7, 1.8, 1.8, 1.9, 1.8,
    1.6, 1.7, 1.7, 1.4, 1.7, 1.7, 1.5, 1.5,
    1.5, 1.5, 1.5, 1.6, 1.6, 1.5, 1.5,
    
    # Improvement scores (1.2-1.6)
    1.4, 1.4, 1.4, 1.3, 1.3, 1.3, 1.2, 1.2,
    1.3, 1.4, 1.5, 1.5, 1.3, 1.2, 1.2,
    
    # Team dynamics scores (1.3-1.7)
    1.3, 1.5, 1.5, 1.6, 1.7, 1.6, 1.6, 1.6,
    1.7, 1.6, 1.6, 1.6, 1.7, 1.7, 1.6, 1.6,
    
    # Emotion scores (1.4-1.8)
    1.7, 1.6, 1.8, 1.7, 1.5, 1.4, 1.4, 1.6, 1.6,
    1.5, 1.6, 1.6, 1.5, 1.5, 1.4, 1.4, 1.4,
    
    # Achievement scores (1.3-1.7)
    1.5, 1.5, 1.6, 1.6, 1.6, 1.5, 1.5, 1.7, 1.5,
    1.4, 1.4, 1.4, 1.4, 1.5, 1.5, 1.5,
    1.4, 1.4, 1.4, 1.4, 1.3, 1.3,
    
    # Game management scores (1.1-1.5)
    1.3, 1.3, 1.3, 1.2, 1.4, 1.4, 1.5, 1.5,
    1.4, 1.4, 1.3, 1.2, 1.1, 1.2, 1.2, 1.2
  ),
  stringsAsFactors = FALSE
)

# Add negative football terms with sentiment scores
negative_terms <- data.frame(
  word = c(
    # Performance-related negative terms
    "lose", "loss", "lost", "defeat", "defeated", "beaten", "fail", "failed", "failure",
    "poor", "bad", "terrible", "awful", "disappointing", "disappointed", "disappointment",
    "struggle", "struggled", "struggling", "weak", "weakness", "inconsistent", "inconsistency",
    "outplayed", "outclassed", "dominated", "overwhelmed", "second-best", 
    
    # Error-related negative terms
    "mistake", "mistakes", "error", "errors", "wrong", "sloppy", "careless", "misplaced",
    "concede", "conceded", "conceding", "penalty", "red card", "sent off", "dismissal",
    "fault", "blame", "missed", "miss", "wasteful", "wasted", 
    
    # Team issue negative terms
    "unorganized", "disorganized", "undisciplined", "ill-disciplined", "unprepared",
    "unbalanced", "disjointed", "disconnected", "divided", "confusion", "confused",
    "pressure", "stressed", "tension", "disarray", "collapse", "collapsed",
    
    # Emotion-related negative terms
    "frustrated", "frustrating", "frustration", "angry", "anger", "upset", "unhappy",
    "disappointed", "disappointing", "worry", "worried", "concern", "concerned",
    "nervous", "anxious", "anxiety", "fear", "doubt", "doubts", "lacking confidence",
    
    # Injury-related negative terms
    "injury", "injuries", "injured", "hurt", "damage", "fitness", "unfit", "tired",
    "fatigue", "exhausted", "exhaustion", "pain", "strain", "overworked", "burnout",
    
    # Game management negative terms
    "unprepared", "tactical error", "wrong tactics", "outcoached", "outmanaged", "naive",
    "inexperienced", "unprofessional", "lack of effort", "gave up", "surrender",
    "unfocused", "distracted", "complacent", "overconfident", "underestimated"
  ),
  sentiment_score = c(
    # Performance scores (-2.0 to -1.5)
    -1.9, -1.9, -1.9, -1.8, -1.8, -1.8, -1.7, -1.7, -1.7,
    -1.7, -1.7, -1.9, -1.9, -1.8, -1.8, -1.8,
    -1.6, -1.6, -1.6, -1.5, -1.5, -1.6, -1.6,
    -1.7, -1.8, -1.7, -1.7, -1.6,
    
    # Error scores (-1.7 to -1.3)
    -1.7, -1.7, -1.7, -1.7, -1.5, -1.6, -1.6, -1.5,
    -1.6, -1.6, -1.6, -1.5, -1.7, -1.7, -1.7,
    -1.5, -1.6, -1.4, -1.4, -1.5, -1.5,
    
    # Team issue scores (-1.7 to -1.4)
    -1.6, -1.6, -1.7, -1.7, -1.6,
    -1.5, -1.6, -1.6, -1.7, -1.5, -1.5,
    -1.4, -1.5, -1.5, -1.6, -1.7, -1.7,
    
    # Emotion scores (-1.8 to -1.3)
    -1.7, -1.7, -1.7, -1.8, -1.8, -1.6, -1.6,
    -1.8, -1.8, -1.5, -1.5, -1.5, -1.5,
    -1.4, -1.5, -1.5, -1.5, -1.4, -1.4, -1.6,
    
    # Injury scores (-1.7 to -1.2)
    -1.7, -1.7, -1.7, -1.6, -1.6, -1.5, -1.6, -1.4,
    -1.5, -1.6, -1.6, -1.5, -1.5, -1.5, -1.6,
    
    # Game management scores (-1.6 to -1.3)
    -1.6, -1.6, -1.5, -1.5, -1.5, -1.4,
    -1.3, -1.5, -1.6, -1.5, -1.5,
    -1.4, -1.4, -1.4, -1.3, -1.4
  ),
  stringsAsFactors = FALSE
)

# Add neutral or context-dependent terms
neutral_terms <- data.frame(
  word = c(
    "match", "game", "fixture", "competition", "tournament", "cup", "league", 
    "play", "played", "playing", "performance", "result", "minutes", "half", 
    "player", "players", "squad", "team", "manager", "coach", "staff", 
    "home", "away", "draw", "training", "season", "transfer", "signing", 
    "pressure", "challenge", "difficult", "tough", "hard", "intensity"
  ),
  sentiment_score = rep(0, 34),
  stringsAsFactors = FALSE
)

# Combine all terms
domain_lexicon <- rbind(positive_terms, negative_terms, neutral_terms)

# Write to CSV
write.csv(domain_lexicon, "domain_lexicon.csv", row.names = FALSE)

cat("Domain lexicon created with", nrow(domain_lexicon), "terms\n")
cat("- Positive terms:", nrow(positive_terms), "\n")
cat("- Negative terms:", nrow(negative_terms), "\n")
cat("- Neutral terms:", nrow(neutral_terms), "\n")
cat("Saved to domain_lexicon.csv\n")

# Show sample of the lexicon
cat("\nSample of positive terms:\n")
print(head(positive_terms, 10))

cat("\nSample of negative terms:\n")
print(head(negative_terms, 10))

# Return the lexicon
domain_lexicon
