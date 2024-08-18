# UltimateMath Project Documentation

## Project Overview

**UltimateMath** is a development framework designed for generating mathematical problems and solutions. By processing the MATH seed dataset, it generates prompts for interaction with large language models (LLMs), ultimately creating new math problems and their corresponding answers. The core of this project involves using LLMs to extract topics and knowledge points from the MATH seed dataset, constructing a knowledge graph, and then performing random walk sampling on this graph to generate new mathematical problems.

**UltimateMath** provides a flexible framework that allows developers to build upon existing features and extend functionality. The framework supports asynchronous concurrent processing of requests and responses, enabling developers to focus on implementing business logic, specifically in data preprocessing and postprocessing, without worrying about the intricacies of network requests. This significantly reduces workload while improving the maintainability and reliability of the project.

## Project Structure

The directory structure of the project is as follows:

```
UltimateMath/
│
├── files/
│   ├── GSM8K.parquet         # Stores the original MATH dataset
│   ├── math_extraction.json  # Stores extracted topics and knowledge points
│   └── math_generation.json  # Stores generated math problems and solutions
│
├── handlers/
│   ├── data_extractor.py     # Handles data extraction from responses (postprocessing)
│   └── data_preparator.py    # Handles message construction (preprocessing)
│
├── network/
│   ├── payload_builder.py    # Builds request payloads
│   ├── request_manager.py    # Manages concurrent requests
│   └── response_handler.py   # Contains decorators and functions for handling responses
│
├── utils/
│   └── graph_algorithm.py    # Implements knowledge graph construction and random walk sampling
│
├── app.py                    # Main program entry point
├── config.py                 # Configuration file for API request settings
└── prompt.py                 # Defines prompt templates and related configurations
```

## File Descriptions

### `app.py`

`app.py` is the main entry point of the project. This file is responsible for invoking the message construction functions in `data_preparator.py`, passing the generated message list to the `retrieve_responses` function in `response_handler.py`, and then processing the response data using functions from `data_extractor.py`. Here is an example of how to use `app.py`:

```python
messages_list, metadata_list = construct_math_generation_messages(num=100)
asyncio.run(retrieve_responses(messages_list, metadata_list, extract_question_and_answer))
```

In this way, developers can easily generate data and extend functionality as needed. When new business requirements arise, simply add new data processing functions in `data_preparator.py` or `data_extractor.py` without modifying the network logic code.

### `config.py`

The `config.py` file contains project configuration settings, including the API request URL, authorization token, the model to use, and the maximum number of concurrent requests. Developers can adjust these settings according to their needs.

### `prompt.py`

The `prompt.py` file is used to define templates for generating prompts. It includes templates for generating math problems and extracting topics and knowledge points, as well as configurations for various problem types and difficulty levels.

### `handlers/data_preparator.py`

The `data_preparator.py` file is responsible for data preprocessing. It contains functions for constructing messages for math extraction and math problem generation. These functions generate a specified number of messages and metadata.

### `handlers/data_extractor.py`

The `data_extractor.py` file is responsible for data postprocessing. It contains functions for extracting topics, knowledge points, questions, and answers from LLM responses. The processed data is stored in the `math_extraction.json` and `math_generation.json` files.

### `network/payload_builder.py`

The `payload_builder.py` file is responsible for building the payloads for API requests. It generates JSON structures that conform to API requirements based on the input message list.

### `network/request_manager.py`

The `request_manager.py` file is responsible for managing concurrent API requests. It uses the `aiohttp` library to handle asynchronous requests and responses and employs a semaphore to limit the number of concurrent requests.

### `network/response_handler.py`

The `response_handler.py` file contains decorators and functions for processing API responses. The `process_response` decorator extracts data from the response and passes it to the processing function. This file also provides the `retrieve_responses` function for batch processing messages and obtaining responses.

### `utils/graph_algorithm.py`

The `graph_algorithm.py` file provides algorithms for constructing knowledge graphs and performing random walk sampling on the graphs. These algorithms are used to generate math problems related to specific topics and knowledge points.

## Usage Instructions

When using this framework, developers should pay attention to the following:

1. **Configuration File**: Set the API request URL, authorization token, and other necessary parameters in `config.py` according to the project requirements.
2. **Preprocessing and Postprocessing**: If new data processing needs arise, add new functions in `handlers/data_preparator.py` and `handlers/data_extractor.py` without modifying the network logic code.
3. **Prompt Templates**: Define and adjust the templates for generating prompts in `prompt.py` to fit different tasks.
4. **Running the Project**: Run the `app.py` file to execute the entire project workflow, generating and processing math problems.

## Contribution Guide

Developers are welcome to contribute to the UltimateMath project by improving and extending it. Before submitting code, please follow the project's structure and style guidelines and test your code to ensure it functions correctly.

## License

This project is open-source under the [MIT License](LICENSE), allowing you to freely use, modify, and distribute the code.

---

Through this development framework, developers can easily leverage large language models to generate new math problems. We encourage you to explore the code and customize or extend it according to your needs.