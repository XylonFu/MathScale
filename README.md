# UltimateMath

**UltimateMath** is a development framework designed to leverage Large Language Models (LLMs) for generating and processing mathematical problems. It utilizes a seed dataset (MATH) to extract topics, knowledge points, and related concepts, then constructs a knowledge graph and performs random walk sampling to produce new math problems aligned with specified topics and difficulty levels. The framework streamlines the pipeline from raw data extraction to problem generation and postprocessing, enabling easy integration, customization, and scaling.

**Key Features:**

- **Seamless Integration of LLMs:**  
  Use LLMs to extract topics, knowledge points, and generate new math problems.
  
- **Asynchronous Concurrent Requests:**  
  Efficiently handle multiple requests to LLM APIs in parallel, facilitating large-scale data processing.
  
- **Customizable Prompts and Metadata:**  
  Easily configure prompts, difficulty levels, question types, and other metadata to tailor generated problems.
  
- **Knowledge Graph Construction and Random Walk Sampling:**  
  Automatically build a concept graph and perform random walk sampling to identify related topics and knowledge points.  
  *This component is a faithful reproduction of the approach described in:*
  
  > Tang, Zhengyang, Xingxing Zhang, Benyou Wang, and Furu Wei. “Mathscale: Scaling instruction tuning for mathematical reasoning.” *arXiv preprint arXiv:2403.02884 (2024).*
  
- **Modular Architecture:**  
  Clear separation of data preprocessing, network requests, and response postprocessing for maintainability and extensibility.

---

## Project Structure

```
UltimateMath/
│
├── files/
│   ├── MATH.json              # Merged MATH dataset file
│   ├── math_extraction.json   # Extracted topics and knowledge points from MATH
│   └── math_generation.json   # Generated math problems and solutions
│
├── handlers/
│   ├── data_extractor.py      # Postprocessing: Extracts data (topics, KPs, questions, answers) from responses
│   └── data_preparator.py     # Preprocessing: Constructs messages and metadata for API requests
│
├── network/
│   ├── payload_builder.py     # Builds JSON payloads for LLM API requests
│   ├── request_manager.py     # Manages asynchronous, concurrent API requests
│   └── response_handler.py    # Decorators and utilities for processing LLM responses
│
├── utils/
│   └── graph_algorithm.py     # Builds concept graphs and performs random walk sampling
│
├── app.py                     # Main application entry point
├── config.py                  # Configuration (API URL, model, headers, concurrency limits)
└── prompt.py                  # Prompt templates and configurations for generation and extraction
```

---

## Core Workflow

1. **Prepare the Dataset:**  
   Start with the MATH dataset. Merge JSON files if necessary and ensure the dataset is loaded into `files/MATH.json`.

2. **Data Extraction (Topics & Knowledge Points):**  
   Use `construct_math_extraction_messages` from `data_preparator.py` to generate prompts for extraction.  
   Run:
   ```python
   messages_list, metadata_list = construct_math_extraction_messages(
       file_path="files/MATH.json",
       required_fields={'question': 'problem', 'answer': 'solution', 'id': 'id'},
       num=100
   )
   ```
   Then send these messages to the API:
   ```python
   import asyncio
   from handlers.data_extractor import extract_topics_and_knowledge_points
   from network.response_handler import retrieve_responses

   asyncio.run(retrieve_responses(messages_list, metadata_list, extract_topics_and_knowledge_points))
   ```
   Extracted data (topics and knowledge points) will be saved in `files/math_extraction.json`.

3. **Concept Graph Construction & Random Walk Sampling:**  
   Build a concept graph from the extracted data and sample related concepts using `build_concept_graph` and `random_walk_sampling` from `utils/graph_algorithm.py`.  
   *This step implements the method described by Tang et al. (2024).*

4. **Problem Generation:**  
   Use `construct_math_generation_messages` to create prompts for generating new math questions aligned with specific types, difficulty levels, topics, and knowledge points:
   ```python
   messages_list, metadata_list = construct_math_generation_messages(num=100)
   ```
   Then run:
   ```python
   from handlers.data_extractor import extract_question_and_answer
   asyncio.run(retrieve_responses(messages_list, metadata_list, extract_question_and_answer))
   ```
   Newly generated problems and answers will be stored in `files/math_generation.json`.

---

## Configuration

**`config.py`**  
- **API_URL:** Endpoint for the LLM API.  
- **HEADERS:** HTTP headers including authorization token.  
- **DEFAULT_PAYLOAD:** Default request parameters, including the model to be used.  
- **MAX_CONCURRENT_REQUESTS:** Controls the level of concurrency for API calls.

Modify `config.py` according to your environment and credentials.

---

## Prompt Templates and Customization

**`prompt.py`**  
- **MATH_EXTRACTION_PROMPT & MATH_GENERATION_PROMPT:**  
  Templates guiding the LLM to extract topics or generate new questions and answers.
  
- **`question_types` & `difficulty_levels`:**  
  Dictionaries defining various problem types and difficulty levels. Adjust or extend these to produce different classes of problems.

---

## Extending and Adapting

- **Preprocessing:**  
  To adapt the system for new datasets or fields, modify or create functions in `data_preparator.py`.
  
- **Postprocessing:**  
  For new extraction logic or additional data fields, edit or add methods in `data_extractor.py`.
  
- **Networking and Payloads:**  
  If the target API or model changes, adjust `payload_builder.py` and `config.py` accordingly. The core request and response flow is maintained in `request_manager.py` and `response_handler.py`.

---

## Citation

If you use the concept graph and random walk sampling approach from this codebase, please cite the referenced paper:

```
@article{tang2024mathscale,
  title={Mathscale: Scaling instruction tuning for mathematical reasoning},
  author={Tang, Zhengyang and Zhang, Xingxing and Wang, Benyou and Wei, Furu},
  journal={arXiv preprint arXiv:2403.02884},
  year={2024}
}
```

---

## License

This project is released under the [MIT License](LICENSE). You are free to use, modify, and distribute the code as permitted by the terms of the license.

---

**UltimateMath** simplifies and scales the creation, extraction, and generation of math problems using LLMs. By integrating a proven concept graph construction and random walk sampling approach, it offers a robust and extensible environment for researchers and educators looking to develop advanced mathematical reasoning tasks.