# Working with Tools in EvoAgentX

This tutorial walks you through using EvoAgentX's powerful tool ecosystem. Tools allow agents to interact with the external world, perform computations, and access information. We'll cover:

1. **Understanding the Tool Architecture**: Learn about the base Tool class and its functionality
2. **Code Interpreters**: Execute Python code safely using Python and Docker interpreters
3. **Search Tools**: Access information from the web using Wikipedia and Google search tools
4. **MCP Tools**: Connect to external services using the Model Context Protocol

By the end of this tutorial, you'll understand how to leverage these tools in your own agents and workflows.

---

## 1. Understanding the Tool Architecture

At the core of EvoAgentX's tool ecosystem is the `Tool` base class, which provides a standardized interface for all tools. 

```python
from evoagentx.tools.tool import Tool
```

The `Tool` class implements three key methods:

- `get_tool_schemas()`: Returns OpenAI-compatible function schemas for the tool
- `get_tools()`: Returns a list of callable functions that the tool provides
- `get_tool_descriptions()`: Returns descriptions of the tool's functionality

All tools in EvoAgentX extend this base class, ensuring a consistent interface for agents to use them.

### Key Concepts

- **Tool Integration**: Tools seamlessly integrate with agents via function calling protocols
- **Schemas**: Each tool provides schemas that describe its functionality, parameters, and outputs
- **Modularity**: Tools can be easily added to any agent that supports function calling

---

## 2. Code Interpreters

EvoAgentX provides two main code interpreter tools:

1. **PythonInterpreter**: Executes Python code in a controlled environment
2. **DockerInterpreter**: Executes code within isolated Docker containers

### 2.1 PythonInterpreter

**The PythonInterpreter provides a secure environment for executing Python code with fine-grained control over imports, directory access, and execution context. It uses a sandboxing approach to restrict potentially harmful operations.**

#### 2.1.1 Setup

```python
from evoagentx.tools.interpreter_python import PythonInterpreter

# Initialize with specific allowed imports and directory access
interpreter = PythonInterpreter(
    project_path=".",  # Default is current directory
    directory_names=["examples", "evoagentx"],
    allowed_imports={"os", "sys", "math", "random", "datetime"}
)
```

#### 2.1.2 Available Methods

The `PythonInterpreter` provides the following callable methods:

##### Method 1: execute(code, language)

**Description**: Executes Python code directly in a secure environment.

**Usage Example**:
```python
# Execute a simple code snippet
result = interpreter.execute("""
print("Hello, World!")
import math
print(f"The value of pi is: {math.pi:.4f}")
""", "python")

print(result)
```

**Return Type**: `str`

**Sample Return**:
```
Hello, World!
The value of pi is: 3.1416
```

---

##### Method 2: execute_script(file_path, language)

**Description**: Executes a Python script file in a secure environment.

**Usage Example**:
```python
# Execute a Python script file
script_path = "examples/hello_world.py"
script_result = interpreter.execute_script(script_path, "python")
print(script_result)
```

**Return Type**: `str`

**Sample Return**:
```
Running hello_world.py...
Hello from the script file!
Script execution completed.
```

#### 2.1.3 Setup Hints

- **Project Path**: The `project_path` parameter should point to the root directory of your project to ensure proper file access. Default is the current directory (".").

- **Directory Names**: The `directory_names` list specifies which directories within your project can be imported from. This is important for security to prevent unauthorized access. Default is an empty list `[]`.

- **Allowed Imports**: The `allowed_imports` set restricts which Python modules can be imported in executed code. Default is an empty list `[]`.
  - **Important**: If `allowed_imports` is set to an empty list, no import restrictions are applied.
  - When specified, add only the modules you consider safe:

```python
# Example with restricted imports
interpreter = PythonInterpreter(
    project_path=os.getcwd(),
    directory_names=["examples", "evoagentx", "tests"],
    allowed_imports={
        "os", "sys", "time", "datetime", "math", "random", 
        "json", "csv", "re", "collections", "itertools"
    }
)

# Example with no import restrictions
interpreter = PythonInterpreter(
    project_path=os.getcwd(),
    directory_names=["examples", "evoagentx"],
    allowed_imports=[]  # Allows any module to be imported
)
```

---

### 2.2 DockerInterpreter

**The DockerInterpreter executes code in isolated Docker containers, providing maximum security and environment isolation. It allows safe execution of potentially risky code with custom environments, dependencies, and complete resource isolation. Docker must be installed and running on your machine to use this tool.**

#### 2.2.1 Setup

```python
from evoagentx.tools.interpreter_docker import DockerInterpreter

# Initialize with a specific Docker image
interpreter = DockerInterpreter(
    image_tag="fundingsocietiesdocker/python3.9-slim",
    print_stdout=True,
    print_stderr=True,
    container_directory="/app"
)
```

#### 2.2.2 Available Methods

The `DockerInterpreter` provides the following callable methods:

##### Method 1: execute(code, language)

**Description**: Executes code inside a Docker container.

**Usage Example**:
```python
# Execute Python code in a Docker container
result = interpreter.execute("""
import platform
print(f"Python version: {platform.python_version()}")
print(f"Platform: {platform.system()} {platform.release()}")
""", "python")

print(result)
```

**Return Type**: `str`

**Sample Return**:
```
Python version: 3.9.16
Platform: Linux 5.15.0-1031-azure
```

---

##### Method 2: execute_script(file_path, language)

**Description**: Executes a script file inside a Docker container.

**Usage Example**:
```python
# Execute a Python script file in Docker
script_path = "examples/docker_test.py"
script_result = interpreter.execute_script(script_path, "python")
print(script_result)
```

**Return Type**: `str`

**Sample Return**:
```
Running container with script: /app/script_12345.py
Hello from the Docker container!
Container execution completed.
```

#### 2.2.3 Setup Hints

- **Docker Requirements**: Ensure Docker is installed and running on your system before using this interpreter.

- **Image Management**: You need to provide **either** an `image_tag` **or** a `dockerfile_path`, not both:
  - **Option 1: Using an existing image**
    ```python
    interpreter = DockerInterpreter(
        image_tag="python:3.9-slim",  # Uses an existing Docker Hub image
        container_directory="/app"
    )
    ```
  
  - **Option 2: Building from a Dockerfile**
    ```python
    interpreter = DockerInterpreter(
        dockerfile_path="path/to/Dockerfile",  # Builds a custom image
        image_tag="my-custom-image-name",      # Name for the built image
        container_directory="/app"
    )
    ```

- **File Access**:
  - To make local files available in the container, use the `host_directory` parameter:
  ```python
  interpreter = DockerInterpreter(
      image_tag="python:3.9-slim",
      host_directory="/path/to/local/files",
      container_directory="/app/data"
  )
  ```
  - This mounts the local directory to the specified container directory, making all files accessible.

- **Container Lifecycle**:
  - The Docker container is created when you initialize the interpreter and removed when the interpreter is destroyed.
  - For long-running sessions, you can set `print_stdout` and `print_stderr` to see real-time output.

- **Troubleshooting**:
  - If you encounter permission issues, ensure your user has Docker privileges.
  - For network-related errors, check if your Docker daemon has proper network access.

---

## 3. Search Tools

EvoAgentX provides several search tools to retrieve information from various sources:

1. **SearchWiki**: Search Wikipedia for information
2. **SearchGoogle**: Search Google using the official API
3. **SearchGoogleFree**: Search Google without requiring an API key

### 3.1 SearchWiki

**The SearchWiki tool retrieves information from Wikipedia articles, providing summaries, full content, and metadata. It offers a straightforward way to incorporate encyclopedic knowledge into your agents without complex API setups.**

#### 3.1.1 Setup

```python
from evoagentx.tools.search_wiki import SearchWiki

# Initialize with custom parameters
wiki_search = SearchWiki(max_sentences=3)
```

#### 3.1.2 Available Methods

The `SearchWiki` provides the following callable method:

##### Method: search(query)

**Description**: Searches Wikipedia for articles matching the query.

**Usage Example**:
```python
# Search Wikipedia for information
results = wiki_search.search(
    query="artificial intelligence agent architecture"
)

# Process the results
for i, result in enumerate(results.get("results", [])):
    print(f"Result {i+1}: {result['title']}")
    print(f"Summary: {result['summary']}")
    print(f"URL: {result['url']}")
```

**Return Type**: `dict`

**Sample Return**:
```python
{
    "results": [
        {
            "title": "Artificial intelligence",
            "summary": "Artificial intelligence (AI) is the intelligence of machines or software, as opposed to the intelligence of humans or animals. AI applications include advanced web search engines, recommendation systems, voice assistants...",
            "url": "https://en.wikipedia.org/wiki/Artificial_intelligence"
        },
        {
            "title": "Intelligent agent",
            "summary": "In artificial intelligence, an intelligent agent (IA) is anything which can perceive its environment, process those perceptions, and respond in pursuit of its own goals...",
            "url": "https://en.wikipedia.org/wiki/Intelligent_agent"
        }
    ]
}
```

---

### 3.2 SearchGoogle

**The SearchGoogle tool enables web searches through Google's official Custom Search API, providing high-quality search results with content extraction. It requires API credentials but offers more reliable and comprehensive search capabilities.**

#### 3.2.1 Setup

```python
from evoagentx.tools.search_google import SearchGoogle

# Initialize with custom parameters
google_search = SearchGoogle(
    num_search_pages=3,
    max_content_words=200
)
```

#### 3.2.2 Available Methods

The `SearchGoogle` provides the following callable method:

##### Method: search(query)

**Description**: Searches Google for content matching the query.

**Usage Example**:
```python
# Search Google for information
results = google_search.search(
    query="evolutionary algorithms for neural networks"
)

# Process the results
for i, result in enumerate(results.get("results", [])):
    print(f"Result {i+1}: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content: {result['content'][:150]}...")
```

**Return Type**: `dict`

**Sample Return**:
```python
{
    "results": [
        {
            "title": "Evolutionary Algorithms for Neural Networks - A Systematic Review",
            "url": "https://example.com/paper1",
            "content": "This paper provides a comprehensive review of evolutionary algorithms applied to neural network optimization. Key approaches include genetic algorithms, particle swarm optimization, and differential evolution..."
        },
        {
            "title": "Applying Genetic Algorithms to Neural Network Training",
            "url": "https://example.com/article2",
            "content": "Genetic algorithms offer a powerful approach to optimizing neural network architectures and weights. This article explores how evolutionary computation can overcome limitations of gradient-based methods..."
        }
    ]
}
```

#### 3.2.3 Setup Hints

- **API Requirements**: This tool requires Google Custom Search API credentials. Set them in your environment:
  ```python
  # In your .env file or environment variables
  GOOGLE_API_KEY=your_google_api_key_here
  GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
  ```

- **Obtaining Credentials**:
  1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
  2. Enable the Custom Search API
  3. Create API credentials
  4. Set up a Custom Search Engine at [https://cse.google.com/cse/](https://cse.google.com/cse/)

---

### 3.3 SearchGoogleFree

**The SearchGoogleFree tool provides web search capability without requiring any API keys or authentication. It offers a simpler alternative to the official Google API with basic search results suitable for most general queries.**

#### 3.3.1 Setup

```python
from evoagentx.tools.search_google_f import SearchGoogleFree

# Initialize the free Google search
google_free = SearchGoogleFree(
    num_search_pages=3,
    max_content_words=500
)
```

#### 3.3.2 Available Methods

The `SearchGoogleFree` provides the following callable method:

##### Method: search(query)

**Description**: Searches Google for content matching the query without requiring an API key.

**Usage Example**:
```python
# Search Google without an API key
results = google_free.search(
    query="reinforcement learning algorithms"
)

# Process the results
for i, result in enumerate(results.get("results", [])):
    print(f"Result {i+1}: {result['title']}")
    print(f"URL: {result['url']}")
```

**Return Type**: `dict`

**Sample Return**:
```python
{
    "results": [
        {
            "title": "Introduction to Reinforcement Learning Algorithms",
            "url": "https://example.com/intro-rl",
            "snippet": "A comprehensive overview of reinforcement learning algorithms including Q-learning, SARSA, and policy gradient methods."
        },
        {
            "title": "Top 10 Reinforcement Learning Algorithms for Beginners",
            "url": "https://example.com/top-rl",
            "snippet": "Learn about the most commonly used reinforcement learning algorithms with practical examples and implementation tips."
        }
    ]
}
```

---

## 4. MCP Tools

**The Model Context Protocol (MCP) toolkit provides a standardized way to connect to external services through the MCP protocol. It enables agents to access specialized tools like job search services, data processing utilities, and other MCP-compatible APIs without requiring direct integration of each service.**

### 4.1 MCPToolkit

#### 4.1.1 Setup

```python
from evoagentx.tools.mcp import MCPToolkit

# Initialize with a configuration file
mcp_toolkit = MCPToolkit(config_path="examples/sample_mcp.config")

# Or initialize with a configuration dictionary
config = {
    "mcpServers": {
        "hirebase": {
            "command": "uvx",
            "args": ["hirebase-mcp"],
            "env": {"HIREBASE_API_KEY": "your_api_key_here"}
        }
    }
}
mcp_toolkit = MCPToolkit(config=config)
```

#### 4.1.2 Available Methods

The `MCPToolkit` provides the following callable methods:

##### Method 1: get_tools()

**Description**: Returns a list of all available tools from connected MCP servers.

**Usage Example**:
```python
# Get all available MCP tools
tools = mcp_toolkit.get_tools()

# Display available tools
for i, tool in enumerate(tools):
    print(f"Tool {i+1}: {tool.name}")
    print(f"Description: {tool.descriptions[0]}")
```

**Return Type**: `List[Tool]`

**Sample Return**:
```
[MCPTool(name="HirebaseSearch", descriptions=["Search for job information by providing keywords"]), 
 MCPTool(name="HirebaseAnalyze", descriptions=["Analyze job market trends for given skills"])]
```

---

##### Method 2: disconnect()

**Description**: Disconnects from all MCP servers and cleans up resources.

**Usage Example**:
```python
# When done with the MCP toolkit
mcp_toolkit.disconnect()
```

**Return Type**: `None`

#### 4.1.3 Using MCP Tools

Once you have obtained the tools from the MCPToolkit, you can use them like any other EvoAgentX tool:

```python
# Get all tools from the toolkit
tools = mcp_toolkit.get_tools()

# Find a specific tool
hirebase_tool = None
for tool in tools:
    if "hire" in tool.name.lower() or "search" in tool.name.lower():
        hirebase_tool = tool
        break

if hirebase_tool:
    # Use the tool to search for information
    search_query = "data scientist"
    result = hirebase_tool.tools[0](**{"query": search_query})
    
    print(f"Search results for '{search_query}':")
    print(result)
```

#### 4.1.4 Setup Hints

- **Configuration File**: The configuration file should follow the MCP protocol's server configuration format:
  ```json
  {
      "mcpServers": {
          "serverName": {
              "command": "executable_command",
              "args": ["command_arguments"],
              "env": {"ENV_VAR_NAME": "value"}
          }
      }
  }
  ```

- **Server Types**:
  - **Command-based servers**: Use the `command` field to specify an executable
  - **URL-based servers**: Use the `url` field to specify a server endpoint

- **Connection Management**:
  - Always call `disconnect()` when you're done using the MCPToolkit to free resources
  - Use a try-finally block for automatic cleanup:
    ```python
    try:
        toolkit = MCPToolkit(config_path="config.json")
        tools = toolkit.get_tools()
        # Use tools here
    finally:
        toolkit.disconnect()
    ```

- **Error Handling**:
  - The MCPToolkit will log warning messages if it can't connect to servers
  - It's good practice to implement error handling around tool calls:
    ```python
    try:
        result = tool.tools[0](**{"query": "example query"})
    except Exception as e:
        print(f"Error calling MCP tool: {str(e)}")
    ```

- **Environment Variables**:
  - API keys and other sensitive information can be provided via environment variables in the config
  - You can also set them in your environment before running your application

---

## Summary

In this tutorial, we've explored the tool ecosystem in EvoAgentX:

1. **Tool Architecture**: Understood the base Tool class and its standardized interface
2. **Code Interpreters**: Learned how to execute Python code securely using both Python and Docker interpreters
3. **Search Tools**: Discovered how to access web information using Wikipedia and Google search tools
4. **MCP Tools**: Learned how to connect to external services using the Model Context Protocol

Tools in EvoAgentX extend your agents' capabilities by providing access to external resources and computation. By combining these tools with agents and workflows, you can build powerful AI systems that can retrieve information, perform calculations, and interact with the world.

For more advanced usage and customization options, refer to the [API documentation](../api/tools.md) and explore the examples in the repository. 