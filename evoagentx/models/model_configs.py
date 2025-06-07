from pydantic import BaseModel, Field
from typing import Optional, Union, List

# import torch 

from ..core.base_config import BaseConfig


#### LLM Configs
class LLMConfig(BaseConfig):

    llm_type: str
    model: str 
    output_response: bool = Field(default=False, description="Whether to output LLM response.")


class OpenAILLMConfig(LLMConfig):

    llm_type: str = "OpenAILLM"
    openai_key: Optional[str] = Field(default=None, description="the API key used to authenticate OpenAI requests")

    # generation parameters
    temperature: Optional[float] = Field(default=None, description="the temperature used to scaling logits")
    max_tokens : Optional[int] = Field(default=None, description="maximum number of generated tokens. This value is now deprecated in favor of max_completion_tokens, and is not compatible with o1 series models.")
    max_completion_tokens: Optional[int] = Field(default=None, description="An upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens. Commonly used in OpenAI's o1 series models.")
    top_p: Optional[float] = Field(default=None, description="Only sample from tokens with cumulative probability greater than top_p when generating text.")
    n: Optional[int] = Field(default=None, description="How many chat completion choices to generate for each input message.")
    stream: Optional[bool] = Field(default=None, description=" If set to true, it sends partial message deltas. Tokens will be sent as they become available, with the stream terminated by a [DONE] message.")
    stream_options: Optional[dict] = Field(default=None, description="Options for streaming response. Only set this when you set stream: true")
    timeout: Optional[Union[float, int]] = Field(default=None, description="Timeout in seconds for completion requests (Defaults to 600 seconds)")

    # tools 
    tools: Optional[List] = Field(default=None, description="A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for.")
    tool_choice: Optional[str] = Field(default=None, description="Controls which (if any) function is called by the model. none means the model will not call a function and instead generates a message. auto means the model can pick between generating a message or calling a function. Specifying a particular function via {\"type\": \"function\", \"function\": {\"name\": \"my_function\"}} forces the model to call that function.")
    parallel_tool_calls: Optional[bool] = Field(default=None, description="Whether to enable parallel function calling during tool use. OpenAI default is true.")
    
    # reasoning parameters 
    reasoning_effort: Optional[str] = Field(default=None, description="Constrains effort on reasoning for reasoning models. Currently supported values are low, medium, and high. Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.")

    # token probabilities
    logprobs: Optional[bool] = Field(default=None, description="Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the content of message.")
    top_logprobs: Optional[int] = Field(default=None, description="An integer between 0 and 5 specifying the number of most likely tokens to return at each token position, each with an associated log probability. logprobs must be set to true if this parameter is used.")

    # predicted outputs 
    prediction: Optional[dict] = Field(default=None, description="Configuration for a Predicted Output, which can greatly improve response times when large parts of the model response are known ahead of time. This is most common when you are regenerating a file with only minor changes to most of the content.")

    # output format
    modalities: Optional[List] = Field(default=None, description="Output types that you would like the model to generate for this request. Most models are capable of generating text, which is the default: [\"text\"]")
    response_format: Optional[Union[BaseModel, dict]] = Field(default=None, description=" An object specifying the format that the model must output.")


class LiteLLMConfig(LLMConfig):

    llm_type: str = "LiteLLM"

    # LLM keys
    openai_key: Optional[str] = Field(default=None, description="the API key used to authenticate OpenAI requests")
    anthropic_key: Optional[str] = Field(default=None, description="the API key used to authenticate Anthropic requests")
    deepseek_key: Optional[str] = Field(default=None, description="the API key used to authenticate Deepseek requests")
    gemini_key: Optional[str] = Field(default=None, description="the API key used to authenticate Gemini requests")
    meta_llama_key: Optional[str] = Field(default=None, description="the API key used to authenticate Meta Llama requests")
    openrouter_key: Optional[str] = Field(default=None, description="the API key used to authenticate OpenRouter requests")
    openrouter_base: Optional[str] = Field(default="https://openrouter.ai/api/v1", description="the base URL used to authenticate OpenRouter requests")
    perplexity_key: Optional[str] = Field(default=None, description="the API key used to authenticate Perplexity requests")
    groq_key: Optional[str] = Field(default=None, description="the API key used to authenticate Groq requests")

    # generation parameters 
    temperature: Optional[float] = Field(default=None, description="the temperature used to scaling logits")
    max_tokens : Optional[int] = Field(default=None, description="maximum number of generated tokens")
    max_completion_tokens: Optional[int] = Field(default=None, description="An upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens. Commonly used in OpenAI's o1 series models.")
    top_p: Optional[float] = Field(default=None, description="Only sample from tokens with cumulative probability greater than top_p when generating text.")
    n: Optional[int] = Field(default=None, description="How many chat completion choices to generate for each input message.")
    stream: Optional[bool] = Field(default=None, description=" If set to true, it sends partial message deltas. Tokens will be sent as they become available, with the stream terminated by a [DONE] message.")
    stream_options: Optional[dict] = Field(default=None, description="Options for streaming response. Only set this when you set stream: true")
    timeout: Optional[Union[float, int]] = Field(default=None, description="Timeout in seconds for completion requests (Defaults to 600 seconds)")

    # tools
    tools: Optional[List] = Field(default=None, description="A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for.")
    tool_choice: Optional[str] = Field(default=None, description="Controls which (if any) function is called by the model. none means the model will not call a function and instead generates a message. auto means the model can pick between generating a message or calling a function. Specifying a particular function via {\"type\": \"function\", \"function\": {\"name\": \"my_function\"}} forces the model to call that function.")
    parallel_tool_calls: Optional[bool] = Field(default=None, description="Whether to enable parallel function calling during tool use. OpenAI default is true.")

    # token probabilities
    logprobs: Optional[bool] = Field(default=None, description="Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the content of message.")
    top_logprobs: Optional[int] = Field(default=None, description="An integer between 0 and 5 specifying the number of most likely tokens to return at each token position, each with an associated log probability. logprobs must be set to true if this parameter is used.")

    # output format
    response_format: Optional[Union[BaseModel, dict]] = Field(default=None, description=" An object specifying the format that the model must output.")

    def __str__(self):
        return self.model


class SiliconFlowConfig(LLMConfig):

    # LLM keys
    llm_type: str = "SiliconFlowLLM"
    siliconflow_key: Optional[str] = Field(default=None, description="the API key used to authenticate SiliconFlow requests") 

    # generation parameters 
    temperature: Optional[float] = Field(default=None, description="the temperature used to scaling logits")
    max_tokens : Optional[int] = Field(default=None, description="maximum number of generated tokens")
    max_completion_tokens: Optional[int] = Field(default=None, description="An upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens. Commonly used in OpenAI's o1 series models.")
    top_p: Optional[float] = Field(default=None, description="Only sample from tokens with cumulative probability greater than top_p when generating text.")
    n: Optional[int] = Field(default=None, description="How many chat completion choices to generate for each input message.")
    stream: Optional[bool] = Field(default=None, description=" If set to true, it sends partial message deltas. Tokens will be sent as they become available, with the stream terminated by a [DONE] message.")
    stream_options: Optional[dict] = Field(default=None, description="Options for streaming response. Only set this when you set stream: true")
    timeout: Optional[Union[float, int]] = Field(default=None, description="Timeout in seconds for completion requests (Defaults to 600 seconds)")

    # tools
    tools: Optional[List] = Field(default=None, description="A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for.")
    tool_choice: Optional[str] = Field(default=None, description="Controls which (if any) function is called by the model. none means the model will not call a function and instead generates a message. auto means the model can pick between generating a message or calling a function. Specifying a particular function via {\"type\": \"function\", \"function\": {\"name\": \"my_function\"}} forces the model to call that function.")
    parallel_tool_calls: Optional[bool] = Field(default=None, description="Whether to enable parallel function calling during tool use. OpenAI default is true.")

    # token probabilities
    logprobs: Optional[bool] = Field(default=None, description="Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the content of message.")
    top_logprobs: Optional[int] = Field(default=None, description="An integer between 0 and 5 specifying the number of most likely tokens to return at each token position, each with an associated log probability. logprobs must be set to true if this parameter is used.")

    # output format
    response_format: Optional[Union[BaseModel, dict]] = Field(default=None, description=" An object specifying the format that the model must output.")

    def __str__(self):
        return self.model
        
class LocalQwen3Config(LLMConfig):
    llm_type: str = "Qwen3LLM"
    qwen3_key: Optional[str] = Field(default=None, description="the API key used to authenticat local Qwen3-235B-A22B requests") 

    # generation parameters 
    temperature: Optional[float] = Field(default=None, description="the temperature used to scaling logits")
    max_tokens : Optional[int] = Field(default=None, description="maximum number of generated tokens")
    max_completion_tokens: Optional[int] = Field(default=None, description="An upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens. Commonly used in OpenAI's o1 series models.")
    top_p: Optional[float] = Field(default=None, description="Only sample from tokens with cumulative probability greater than top_p when generating text.")
    n: Optional[int] = Field(default=None, description="How many chat completion choices to generate for each input message.")
    stream: Optional[bool] = Field(default=None, description=" If set to true, it sends partial message deltas. Tokens will be sent as they become available, with the stream terminated by a [DONE] message.")
    stream_options: Optional[dict] = Field(default=None, description="Options for streaming response. Only set this when you set stream: true")
    timeout: Optional[Union[float, int]] = Field(default=None, description="Timeout in seconds for completion requests (Defaults to 600 seconds)")

    # tools
    tools: Optional[List] = Field(default=None, description="A list of tools the model may call. Currently, only functions are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for.")
    tool_choice: Optional[str] = Field(default=None, description="Controls which (if any) function is called by the model. none means the model will not call a function and instead generates a message. auto means the model can pick between generating a message or calling a function. Specifying a particular function via {\"type\": \"function\", \"function\": {\"name\": \"my_function\"}} forces the model to call that function.")
    parallel_tool_calls: Optional[bool] = Field(default=None, description="Whether to enable parallel function calling during tool use. OpenAI default is true.")

    # token probabilities
    logprobs: Optional[bool] = Field(default=None, description="Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the content of message.")
    top_logprobs: Optional[int] = Field(default=None, description="An integer between 0 and 5 specifying the number of most likely tokens to return at each token position, each with an associated log probability. logprobs must be set to true if this parameter is used.")

    # output format
    response_format: Optional[Union[BaseModel, dict]] = Field(default=None, description=" An object specifying the format that the model must output.")

    def __str__(self):
        return self.model

# def get_default_device():
#     return "cuda" if torch.cuda.is_available() else "cpu"

class OpenRouterConfig(LLMConfig):
    llm_type: str = "OpenRouterLLM"
    
    # LLM keys
    openrouter_key: Optional[str] = Field(default=None, description="the API key used to authenticate OpenRouter requests")
    openrouter_base: Optional[str] = Field(default="https://openrouter.ai/api/v1", description="the base URL used to authenticate OpenRouter requests")
    openrouter_model_base: Optional[str] = Field(default="https://openrouter.ai/api/v1/models", description="the model url to access model details")
    # generation parameters 
    temperature: Optional[float] = Field(default=None, description="the temperature used to scaling logits")
    top_p: Optional[float] = Field(default=None, description="This setting limits the model's choices to a percentage of likely tokens: only the top tokens whose probabilities add up to P. A lower value makes the model's responses more predictable, while the default setting allows for a full range of token choices.")
    top_k: Optional[int] = Field(default=None, description="This limits the model's choice of tokens at each step, making it choose from a smaller set. A value of 1 means the model will always pick the most likely next token, leading to predictable results.")
    frequency_penalty: Optional[float] = Field(default=None, description="Controls repetition of tokens based on frequency in input. Range: -2.0 to 2.0. Higher values reduce repetition of frequent tokens.")
    presence_penalty: Optional[float] = Field(default=None, description="Adjusts repetition of specific tokens from input. Range: -2.0 to 2.0. Higher values reduce repetition.")
    repetition_penalty: Optional[float] = Field(default=None, description="Reduces repetition of tokens from input. Range: 0.0 to 2.0. Higher values make repetition less likely.")
    min_p: Optional[float] = Field(default=None, description="Minimum probability for a token relative to most likely token. Range: 0.0 to 1.0.")
    top_a: Optional[float] = Field(default=None, description="Consider only tokens with 'sufficiently high' probabilities based on most likely token. Range: 0.0 to 1.0.")
    seed: Optional[int] = Field(default=None, description="For deterministic sampling. Repeated requests with same seed and parameters should return same result.")
    max_tokens: Optional[int] = Field(default=None, description="Upper limit for number of tokens model can generate. Must be 1 or above.")
    logit_bias: Optional[dict] = Field(default=None, description="Map of token IDs to bias values (-100 to 100) to adjust token selection probabilities.")
    logprobs: Optional[bool] = Field(default=None, description="Whether to return log probabilities of output tokens.")
    top_logprobs: Optional[int] = Field(default=None, description="Number of most likely tokens to return at each position (0-20) with log probabilities.")
    response_format: Optional[Union[BaseModel, dict]] = Field(default=None, description="Forces model to produce specific output format (e.g. JSON mode).")
    structured_outputs: Optional[bool] = Field(default=None, description="Whether model can return structured outputs using response_format json_schema.")
    stop: Optional[List[str]] = Field(default=None, description="Stop generation if model encounters any token in this array.")
    tools: Optional[List] = Field(default=None, description="Tool calling parameter following OpenAI's tool calling request shape.")
    tool_choice: Optional[Union[str, dict]] = Field(default=None, description="Controls which tool is called by model. Can be 'none', 'auto', 'required', or specific tool configuration.")

    stream: Optional[bool] = Field(default=None, description="If set to true, it sends partial message deltas. Tokens will be sent as they become available, with the stream terminated by a [DONE] message.")
    def __str__(self):
        return self.model
