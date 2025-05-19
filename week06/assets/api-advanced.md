# Week 6: Supplementary Information for Introduction to APIs

## HTTP: Client-Server Communication and the Request-Response Cycle

Before diving into APIs, it’s essential to understand how web communication works at its most basic level. The web runs on **HTTP (HyperText Transfer Protocol)**, a simple, text-based language that lets one computer or application (the **client**) ask another computer (the **server**) for data or actions. Whenever you browse a site or call a web service, your client sends an HTTP *request* and the server answers with an HTTP *response*.

An HTTP request consists of a **URL**—the address of the resource or endpoint you want—and an **HTTP method**, which tells the server what you’d like to do. The two most common methods are **GET** (to fetch data, like loading a webpage) and **POST** (to submit data, such as filling in a form). By combining the URL and method (e.g. `GET https://example.com/data`), the client makes its intentions clear.

When the server receives that request, it processes whatever work is needed—retrieving files, querying a database, or running a service—and then sends back a response. Each response begins with a **status code** (a number indicating success or failure, such as **200 OK** for success or **404 Not Found** when something is missing) followed by the **body** containing the actual data or content. For webpages this is usually HTML; for data services (APIs), it’s often JSON (JavaScript Object Notation).

This back-and-forth interaction is called the **request-response cycle**, and it’s entirely **stateless**—each request is handled on its own, with no memory of previous requests. That stateless design makes HTTP simple and highly scalable, allowing any client that speaks HTTP (from browsers to Python scripts) to interoperate with any server that understands HTTP. When you move on to APIs, you’ll leverage this same cycle to automate large-scale data retrieval and processing.

Listen to Alice Evans explain all things HTTP on [this](https://www.softwaresessions.com/episodes/how-http-works-with-julia-evans/) podcast.

## How APIs Work: Client-Server Interaction, Requests, and Responses

At its core, an API works through a **client-server interaction** over the internet. Let’s break down the key concepts:

* **Client and Server:** The **client** is the part that sends a request (this would be your code or application), and the **server** is the part that receives the request and provides a response (this is the API’s service, often running on a remote server or in the cloud). In our context, **you (or your Python script)** are the client, and the **API provider’s system** is the server.
* **Request:** A request is the message the client sends to the server asking for some action or data. Think of it as filling out an order form or making a specific query. A request typically includes:

  * **An endpoint URL** (the address of the API and the specific service you want).
  * **A method/verb** (often one of the HTTP methods like GET to retrieve data or POST to send data).
  * **Parameters or data** (any additional information the server needs, such as the text you want analyzed or a query like a city name for a weather API).
  * **Headers including an API key** if required (more on API keys soon).
* **Response:** After the server receives your request and processes it, it sends back a response. The response contains:

  * **Status code** – a number that tells you if the request was successful (e.g. 200 OK), or if something went wrong (e.g. 404 Not Found, 401 Unauthorized).
  * **Data** – the information you asked for, often in a structured format like JSON (a common text-based data format) or XML. For example, if you requested sentiment analysis, the response data might be a sentiment score or label for your text.
  * **Metadata or messages** – sometimes additional info, like how long the request took or usage details.

&#x20;*Client-Server Communication:* Your application (client) sends an **HTTP request** to an API’s server (for example, asking for sentiment analysis on some text). The server then processes that request and sends back an **HTTP response** containing the result (for instance, the sentiment score). This request-response cycle is the foundation of how we use APIs.

* **API Endpoint:** An **endpoint** is a specific address (URL) that you hit to access a particular service or data from an API. It’s like a function or feature on the server that you can invoke. For example, a sentiment analysis API might have an endpoint like `/analyzeSentiment` that you call to get a sentiment result. Each endpoint usually corresponds to one type of task or data.
* **API Documentation:** Because you can’t see the “kitchen” (the server’s internal code or database), the API documentation is your guide to what you can request and how to format those requests. It typically lists all available endpoints, what parameters they accept, what kind of output they return, and examples. Good documentation is like a user manual for the API.

In summary, using an API is a bit like sending a letter to a remote service (the request) and getting a letter back (the response). Your role as the client is to follow the API’s "letter-writing rules" so the server understands what you want.

## REST APIs: The Common Way to Communicate

When people talk about web APIs, they are often referring to **REST APIs**. **REST** stands for *Representational State Transfer*, which is a style of designing networked applications. You don’t need to remember the term, but here’s what it means in practice:

* **Uses HTTP:** REST APIs use the same protocol your web browser uses – HTTP. This means you’re often calling URLs (web addresses) just like loading a webpage, but instead of a webpage, you get data.
* **Endpoints and Resources:** In a REST API, different URLs (endpoints) represent different **resources** or services. For example, `GET https://api.openweathermap.org/data/2.5/weather?q=London` might retrieve weather data for London. Here, the endpoint `/data/2.5/weather` is a resource for weather info, and `q=London` is a parameter specifying the city.
* **HTTP Methods (Verbs):** REST APIs make use of HTTP methods such as:

  * **GET** – Retrieve data (for example, get information or fetch results; e.g., get the sentiment of a text or fetch a list of comments).
  * **POST** – Send data or create a new resource (for example, submit a new text to be analyzed, or add a new entry to a database via the API).
  * **PUT/PATCH** – Update an existing resource (for example, update a record in a database).
  * **DELETE** – Delete a resource.

  In our sentiment analysis example, you might use a GET request if the text is included in the URL or a POST request if you are sending the text in the request body. The key idea is that the method indicates what action you want to perform on the resource.
* **Stateless Communication:** REST APIs are **stateless**, meaning each request is independent. The server doesn’t retain information about your previous requests. This is like each request being a separate, self-contained transaction. For instance, if you call the sentiment analysis API twice with two different texts, the server doesn’t remember the first text when processing the second – you need to send all the information it needs each time. The stateless design makes it easier to scale and ensures that each server can handle any request without needing to know what came before.

REST APIs are popular because they are simple, scalable, and use existing web standards. Almost any programming environment can send HTTP requests, so REST makes it easy to interact with services from different languages and platforms. When you hear about APIs from providers like Google, Twitter, or OpenAI, they are usually implemented as RESTful APIs.

## Other API Styles: GraphQL and WebSockets

REST is the most common approach, but it’s not the only pattern you might encounter. Here are two other API styles, just for your awareness:

* **GraphQL:** GraphQL is an alternative approach where instead of multiple specific endpoints, you have a single endpoint that can handle flexible queries. You send a query describing exactly what data you want, and you get back precisely that data. This can reduce the number of requests needed for complex apps. For example, if a REST API required you to call one endpoint for user info and another for user posts, a GraphQL API could allow you to get both in a single request by specifying that in the query. It’s powerful for complex data fetching, but also a bit more advanced in usage. (In this course we won’t be using GraphQL, but it’s good to know it exists.)
* **WebSockets (Real-Time APIs):** A WebSocket provides a continuous two-way connection between client and server, allowing data to be sent in real time. This isn’t a request-response model; it’s more like an open channel. WebSockets are useful for applications like live chat, streaming data updates, or multiplayer games – anywhere you want instant, ongoing data flow. For instance, if you were tracking sentiment on a live stream of tweets, a WebSocket connection could stream new analyses continuously. This is more specialized, so we’ll stick to the request/response style in our work, but you might encounter WebSocket APIs in other contexts (e.g., real-time stock price feeds).

For most data analysis tasks (like fetching data or sending data for analysis), you’ll be using **REST APIs**, as they cover the majority of use cases and are easier to get started with.

Great, I’ll put together a conceptual overview of how API client libraries (especially in Python, with a mention of R) work, including when and why you’d use them, and how they simplify HTTP requests behind the scenes. I’ll be back shortly with the draft section you can add to your markdown.

## API Client Libraries

When working with web APIs, you often have the choice of using **API client libraries** instead of crafting raw HTTP requests. An API client library (sometimes called an SDK or helper library) is a package provided in a specific programming language that wraps the API’s functionality in convenient functions or classes. In Python especially, many major services offer official or community-maintained libraries to simplify API usage. These libraries act as a language-specific abstraction layer over the API – they break the API’s usual language-agnostic nature to make the developer experience smoother. In practice, this means you can interact with the API using Python objects and methods, rather than manually formatting HTTP requests and parsing responses.

**Why use a client library?** Client libraries **simplify and reduce the code** you need to write for common API tasks. Instead of manually assembling URLs, query parameters, headers, and JSON payloads for each request, you can call a function or method provided by the library and let it handle those details. For example, a library might provide a method like `get_user_tweets("Alice")` or `openai.ChatCompletion.create(...)` – behind the scenes, that method will construct the proper HTTP request (with the correct endpoint and parameters), send it, and parse the result for you. In other words, the library **“abstracts away the HTTP requests and offers more convenient interfaces”** to work with the API. This abstraction typically covers:

* **Request formatting and transport:** The library builds the correct HTTP requests (URLs, methods, headers, body) and sends them using an HTTP client, so you don’t have to manually use tools like `requests` or `curl`. It also often manages details like authentication headers (API keys, tokens) for you after an initial setup.
* **Response parsing and serialization:** Data returned from the API (usually in JSON) is automatically parsed into Python data structures or objects. Similarly, when you provide data to send (like a dictionary or object), the library serializes it to JSON. This spares you from manual JSON formatting.
* **Error handling and reliability:** Good client libraries include error handling logic. They might raise clear exceptions for error responses (rather than you checking HTTP status codes yourself) and handle common issues like rate limiting or retries. This means your code can focus on **what** you want to do with the API, and the library handles the low-level communication details.
* **Idiomatic interface:** The library’s functions and classes are designed to feel natural in the given language. For instance, Python libraries will return Python objects (like dictionaries or custom classes) and use Python naming conventions. This makes the API **“simple and intuitive to use”** in that language, as opposed to treating everything as raw text or HTTP mechanics.

## Making an API Call: A Conceptual Walkthrough

Let’s put all this into a concrete example without diving into code. How would you use an API for a task, say, analyzing sentiment on a large number of texts? Here’s the high-level process:

1. **Find a Suitable API & Read the Documentation:** First, you’d identify an API that offers sentiment analysis (or whatever task you need). This could be a cloud service like Azure Cognitive Services, IBM Watson NLU, or OpenAI’s API. You’d read the documentation to find out the endpoint for sentiment analysis, what inputs it expects (maybe it requires a piece of text or a list of texts, and possibly a language or other settings), and what the output looks like.
2. **Obtain Access (API Key):** You sign up for the service to get your API key (or other credentials). For example, you might create a free account and receive a key like `abcd1234...` that identifies you.
3. **Construct the Request:** Using the information from the docs, you prepare your API request. For example:

   * Decide on the HTTP method: sentiment analysis might require a **POST** request because you’re sending data (the text).
   * Determine the endpoint URL: e.g., `https://api.some-service.com/v1/sentiment`.
   * Prepare the data format: the API might require JSON. For instance, you might need to send `{"text": "I love this product!"}` in the body of the request. If you have multiple texts, maybe it allows an array of texts.
   * Include your **API key** as instructed (maybe in a header or as a parameter).
4. **Send the Request (Client side):** Now you send the request from your client (which could be a Python script, a command-line tool like `curl`, or an app like Postman for testing). This is when your program reaches out over the internet to the API’s server with your request details.
5. **Receive the Response (Server side):** The API’s server processes your input. It runs the sentiment analysis on the text you sent. Then it sends back a response. Let’s say the response is a JSON object like: `{"sentiment": "positive", "confidence": 0.95}`, along with an HTTP status code 200 (meaning success). If something was wrong (e.g., missing the API key or the text was too long), you might get an error response instead of explaining what went wrong.
6. **Integrate the Results:** Your code receives this response data. Now you can use it in your analysis. For instance, your program can take the `"sentiment": "positive"` value and record that this particular review was positive. You might loop through all 10,000 reviews, call the API for each, and collect the results. In the end, you could calculate statistics (like 60% of reviews are positive, 30% neutral, 10% negative, etc.) or visualize the data.

Throughout this process, the heavy work (the actual sentiment computation) is done by the API provider’s servers. Your job is to correctly send requests and process the responses. In practice, you’d likely write a small script to automate steps 3–6 so that you can handle many texts sequentially or in parallel.

Even without writing code here, hopefully, you can see the pattern: **find API -> get access -> request -> response -> use data**. Once you learn to do this, you can apply it to countless situations, not just sentiment analysis.

[Please see our api-use.md file for fundamental information.](api-use.md)
