# Week 6: Introduction to APIs

## Why APIs?

Previously, we manually examined a sample of just 20 texts and tried using an LLM for sentiment analysis. How long did this take you? Would it still be doable if there were 75 texts? Likely, yes. However, imagine you have **10,000** texts to analyze for sentiment. Analyzing 10,000 texts one by one (or copying them into a tool manually) would be nearly impossible – it would take endless hours and be prone to error. We need a way to **automate and scale** the process. This is where **APIs** come in. By leveraging an API, we can send those thousands of texts to a powerful external service that analyzes sentiment and returns results in seconds. A nice recent example of this in economics research is [a recent working paper](./American%20Life%20Histories%20by%20Lagakos%2C%20Michalopoulos%2C%20and%20Voth.pdf) that used as data over 1,400 American life narratives from the 1930s to uncover common themes about what it means to live a meaningful life.

## What is an API?

An **API (Application Programming Interface)** is like a **messenger** or **middleman** that lets two different programs talk to each other and exchange information. Instead of a person directly doing a task, you have one software program asking another program to do something on its behalf. A popular analogy is that an API is similar to a [**restaurant waiter**](https://www.youtube.com/watch?v=OVvTv9Hy91Q):

* **You (the client)** are sitting at a table, ready to order a meal (you have a request for information or a service).
* **The waiter (the API)** takes your order and relays it to the kitchen. You don’t go into the kitchen yourself – the waiter is the go-between.
* **The kitchen (the server)** is where the work happens. The chef prepares the meal (the data or service you requested).
* **The waiter (API) returns with your meal** and serves it to you. You get exactly what you ordered, without having to know how the kitchen prepared it.

In this analogy, the restaurant’s **menu** is like the **API documentation** – it lists what you can ask for and how to ask for it. If you request something not on the menu, the waiter (API) will tell you it’s not available (an error). Similarly, an API provides a set of **rules and endpoints** that define what requests can be made and what responses you can expect.

This means you don’t need to know the complex inner workings of the server or service. You just need to know *what* to ask for and *how* to ask for it through the API. The API handles the communication, just as the waiter handles communication between you and the kitchen.

## Benefits of Using APIs in Data Analysis

Why use APIs as a data analyst? Here are some key benefits:

* **Scalability:** APIs let you process *large volumes* of data quickly. You can automate requests in code, so analyzing 10,000 texts or more becomes feasible. Instead of manually working with each piece of data, you let a server handle the heavy lifting.
* **Access to Powerful Tools:** Many companies provide APIs for advanced services like sentiment analysis, language translation, image recognition, or data storage. As a data analyst, you can tap into these **pre-built models and services** without having to develop them from scratch.
* **Time and Effort Savings:** Using an API, you can perform complex tasks with just a simple request. This saves you the time of writing extensive code or doing repetitive work. For example, rather than writing your own sentiment analysis algorithm, you can send text to an API and get sentiment results immediately.
* **Integration of Data Sources:** APIs allow different software and datasets to integrate. You can pull data from different sources (e.g. Twitter’s API for tweets, a weather API for climate data) directly into your analysis pipeline. This **marries data from multiple sources** seamlessly.
* **Consistency and Reliability:** When you use a well-established API, you benefit from a service that’s been tested and optimized. The API will handle errors, edge cases, and updates, so you get consistent results. It’s like outsourcing a task to an expert – you trust the API to do its job correctly.

## API Keys and Authentication

Most APIs require some form of **authentication** to ensure that only authorized users or applications can use them. The simplest form is an **API key**. An API key is like a **secret password or ID** that you include with your API calls:

* You typically get an API key by creating an account or registering an application with the API provider. For example, to use the Twitter API or OpenAI API, you’d sign up and receive a key (or token).
* The key itself is usually a long string of characters (letters, numbers, and symbols). It’s unique to you or your application.
* You include this key with every request. Often it goes in a request header (for instance, you might set a header `Authorization: Bearer YOUR_API_KEY`), or sometimes as a URL parameter (e.g., `?api_key=YOUR_API_KEY` in the query string). The API documentation will tell you exactly how to include the key.
* The server checks the key. If the key is missing or wrong, the API will usually respond with an authentication error (like a 401 Unauthorized status). If the key is valid, the server will proceed to handle your request.
* **Security tip:** Never share your API keys publicly or commit them to public repositories. They are meant to be kept secret. If someone obtains your key, they could use the API pretending to be you, which might violate usage limits or incur costs on your account.

Some services use more complex authentication (like OAuth tokens which have limited scope or expiration), but an API key is the fundamental concept to understand first. It’s your **access credential** for using the API.

## Walkthrough examples

1. Very simple from World Bank
2. Simple with AI key from FRED
3. More advanced [Football data]() (python, R)

## R
**Client libraries in other languages:** While our focus is on Python, other programming languages provide similar conveniences. In R, for example, packages like **`httr`** (for making HTTP requests) and **`jsonlite`** (for parsing JSON) are commonly used to work with web APIs. Many APIs also have R packages or wrappers that function like client libraries, letting you call the API in one or two lines of R code. The core idea is the same: a client library abstracts the RESTful requests into native language functions. Regardless of language, using a client library means you can integrate an API into your data analysis or application with less hassle, letting you focus on interpreting results rather than the mechanics of HTTP.

## Scaling Up with APIs: From 20 to 10,000 and Beyond

The introduction of APIs into your workflow transforms what you can accomplish:

* Tasks that were **infeasible by hand** become trivial to automate. You could get results in minutes or hours rather than weeks.
* You can harness **powerful algorithms** provided by industry leaders. For example, instead of developing your machine learning model, you can use Google’s vision API to tag images or OpenAI’s language API to summarize text. This means you can tackle complex problems without needing to be an expert in those specific subfields.
* You can work with **real-time** and **large-scale data**. Want to analyze football statistics or financial market data? There are APIs to fetch those streams of information. With APIs, you are not limited to data you can collect manually; you can pull in data from all over the world programmatically.

APIs are a bridge to practically unlimited data and capabilities. They let your programs communicate with other services to get things done efficiently. As we continue this course, you’ll get hands-on experience using APIs – turning the concepts you learned here into actual data analysis tasks. Embrace this new tool in your skillset. **Whenever you find yourself needing to scale up or access a specialized service, think: *Is there an API for that?*** Chances are, the answer will be yes, and now you’ll know how to use it!

[Please see our api-advanced.md file for more advanced and supplementary information.](api-advanced.md)
