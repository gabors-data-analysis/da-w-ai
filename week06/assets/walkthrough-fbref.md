## Walkthrough: Using `soccerdata` to Fetch Arsenal’s 2023–24 Match Stats

Below is a simple, step-by-step recipe for pulling Arsenal’s match-by-match team statistics for the 2023–24 Premier League season from FBref, using the `soccerdata` Python client library. You never write raw HTTP requests—`soccerdata` handles those for you.

```
# 1. Install and import the library
#    Wraps FBref’s REST API in Python methods.
#    pip install soccerdata
import soccerdata as sd

# 2. Initialize the FBref data source
#    Specify the league and season you want.
fbref = sd.FBref(leagues="ENG-Premier League", seasons="2023-24")

# 3. Retrieve Arsenal’s match stats
#    Returns a pandas DataFrame of every fixture.
arsenal_stats = fbref.read_team_match_stats(team="Arsenal")

# 4. Inspect the resulting DataFrame
print(arsenal_stats.head())
```

### What just happened?

- **Abstraction over HTTP**  
  The `FBref` class builds the correct URLs, attaches any required headers or API keys, sends HTTP GET requests to FBref’s endpoints, and handles pagination and retries automatically.

- **Automatic data parsing**  
  JSON responses from FBref are converted into a pandas DataFrame for you—no manual `json.loads()` or DataFrame construction needed.

- **Error handling & reliability**  
  Common HTTP errors (e.g., timeouts, 404 Not Found) are wrapped in clear exceptions. Transient failures can trigger automatic retries, so your analysis code stays focused on insights, not networking glitches.

- **Idiomatic, Pythonic interface**  
  The library returns native Python objects (DataFrames, lists, dictionaries) and uses familiar method names, making the API feel intuitive and concise rather than a tangle of raw HTTP mechanics.

Under the hood, `soccerdata` still uses an HTTP client (like `requests`) to interact with the REST API. But by encapsulating all networking, authentication, and JSON-handling logic in a single `read_team_match_stats()` call, it lets you:

1. **Write clean, declarative code**  
2. **Develop faster with fewer bugs**  
3. **Focus on analysis and insights instead of HTTP details**

This pattern—installing a client library, instantiating a connector object, invoking a single method, and working with a DataFrame—is common across many Python APIs, from OpenAI to Google Cloud to GitHub. Once you understand it, you can apply it to virtually any web service.

## R equivalent

```
# 1. Install and load the package
install.packages("worldfootballR")  # different package, same idea
library(worldfootballR)

# 2. Get Arsenal match results from the Premier League 2023/24
arsenal_matches <- fb_team_match_results(
  team_url = "https://fbref.com/en/squads/18bb7c10/Arsenal-Stats")

# 3. Inspect the data
head(arsenal_matches)

```
