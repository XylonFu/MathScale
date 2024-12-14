# MathScale

**MathScale** is a development framework designed to leverage Large Language Models (LLMs) for generating, extracting, and processing mathematical problems. It starts with a seed dataset (MATH), from which it extracts topics, knowledge points, and related concepts, builds a concept graph, and performs random walk sampling to generate new, tailored mathematical questions and solutions. The entire pipeline—from data extraction and problem generation to postprocessing—is integrated and highly customizable, making it easier for researchers, educators, and developers to build upon this work.

**Key Features:**

- **LLM-Driven Data Extraction and Generation:**  
  Automatically extract topics and knowledge points from the MATH dataset using LLMs, and generate new math problems aligned with specified topics, difficulty levels, and question types.

- **Asynchronous and Scalable:**  
  Handle multiple LLM requests in parallel using asynchronous operations. This enables large-scale data processing and reduces turnaround time.

- **Customizable Prompts and Metadata:**  
  Fine-tune the prompt templates, difficulty levels, question types, and more. Align generated tasks with specific goals—be it educational, research-oriented, or assessment-related.

- **Concept Graph Construction & Random Walk Sampling (MathScale Approach):**  
  Construct a knowledge graph of extracted concepts and apply random walk sampling to identify interconnected topics and knowledge points.  
  *This methodology is a faithful reproduction of the approach described in the MathScale paper:*
  
  > Tang, Zhengyang, Xingxing Zhang, Benyou Wang, and Furu Wei.  
  > "Mathscale: Scaling instruction tuning for mathematical reasoning."  
  > *arXiv preprint arXiv:2403.02884 (2024).*

- **Modular and Extensible Architecture:**  
  Clearly separated components (preprocessing, request handling, postprocessing) allow easy integration with other datasets, APIs, or LLM services. You can modify prompts, processing steps, and outputs without altering the network handling logic.

---

## Project Structure

```
MathScale/
│
├── files/
│   ├── MATH.json              # Merged MATH dataset
│   ├── math_extraction.json   # Extracted topics and knowledge points
│   └── math_generation.json   # Generated math problems and solutions
│
├── handlers/
│   ├── data_extractor.py      # Postprocessing: Extract data from LLM responses
│   └── data_preparator.py     # Preprocessing: Construct prompts and metadata for LLM requests
│
├── network/
│   ├── payload_builder.py     # Builds JSON payloads for LLM API requests
│   ├── request_manager.py     # Manages asynchronous, concurrent API requests
│   └── response_handler.py    # Decorators and functions for handling LLM responses
│
├── utils/
│   └── graph_algorithm.py     # Builds concept graphs and performs random walk sampling
│
├── app.py                     # Main application entry point
├── config.py                  # Configuration (API URL, headers, model, concurrency limits)
└── prompt.py                  # Prompt templates, question types, and difficulty levels
```

---

## Getting Started

### 1. Prepare the MATH Dataset

1. Place or merge your MATH dataset JSON files under `files/MATH.json`.
2. Adjust `input_directory` and `output_file_path` in the code if needed.

### 2. Extracting Topics and Knowledge Points

**Goal:** Extract topics and knowledge points from existing math problems in `MATH.json`.

```python
from handlers.data_preparator import construct_math_extraction_messages
from handlers.data_extractor import extract_topics_and_knowledge_points
from network.response_handler import retrieve_responses
import asyncio

# Prepare extraction messages
messages_list, metadata_list = construct_math_extraction_messages(
    file_path="files/MATH.json",
    required_fields={'question': 'problem', 'answer': 'solution', 'id': 'id'},
    num=100
)

# Run extraction via LLM
asyncio.run(retrieve_responses(messages_list, metadata_list, extract_topics_and_knowledge_points))
```

Upon completion, `files/math_extraction.json` will contain extracted topics and knowledge points.

### 3. Building the Concept Graph & Random Walk Sampling

**Goal:** Construct a concept graph from extracted data, then sample interconnected topics and knowledge points using random walk. This step is automatic when generating new problems. The code internally calls `build_concept_graph` and `random_walk_sampling` from `utils/graph_algorithm.py` to produce coherent and related sets of concepts.

### 4. Generating New Math Problems

**Goal:** Generate new math problems aligned with chosen difficulty levels, question types, and the extracted topics/knowledge points.

```python
from handlers.data_preparator import construct_math_generation_messages
from handlers.data_extractor import extract_question_and_answer

# Prepare generation messages
messages_list, metadata_list = construct_math_generation_messages(num=100)

# Run generation via LLM
asyncio.run(retrieve_responses(messages_list, metadata_list, extract_question_and_answer))
```

`files/math_generation.json` will contain the newly generated problems and their answers.

---

## Configuration

**`config.py`** provides the core configuration:

- **API_URL:** The LLM service endpoint.
- **HEADERS:** Include authentication tokens if required.
- **DEFAULT_PAYLOAD:** Specify the LLM model and any default parameters.
- **MAX_CONCURRENT_REQUESTS:** Control the concurrency for large-scale batch processing.

Adjust these parameters to match your environment and LLM service.

---

## Customization

**`prompt.py`** allows you to fine-tune the generation and extraction process:

- **MATH_EXTRACTION_PROMPT & MATH_GENERATION_PROMPT:**  
  Predefined templates directing the LLM to extract topics or generate questions/answers.
  
- **`question_types` & `difficulty_levels`:**  
  Dictionaries defining various question types (e.g., Problem-Solving, Proof) and difficulty levels (e.g., Elementary, PhD). Extend or modify these to fit your educational or research objectives.

---

## Extending the Framework

- **Data Preprocessing:**  
  For new datasets or formats, modify `data_preparator.py` to produce the appropriate prompts and metadata.

- **Data Postprocessing:**  
  Need more complex parsing or additional metadata fields? Edit `data_extractor.py` to adapt extraction logic from LLM responses.

- **Network and Payload Adaptation:**  
  If you switch to a different LLM provider or model, adjust `payload_builder.py` and `config.py`. The request and response handling logic remains the same, ensuring minimal disruption.

---

## Citation

If you use the concept graph and random walk sampling methods in this codebase, please cite the MathScale paper:

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

This project is available under the [MIT License](LICENSE). You are free to use, modify, and distribute the code as permitted by the terms of the license.

---

**MathScale** streamlines the LLM-driven math problem generation process. By incorporating concept graphs and random walk sampling based on the MathScale approach, it provides a robust, scalable, and flexible platform for educators, researchers, and developers to produce advanced mathematical content.