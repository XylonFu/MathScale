# UltimateMath

**UltimateMath** 是一个开发框架，旨在利用大型语言模型（LLM）来生成和处理数学问题。该框架从 MATH 基础数据集中提取相关主题与知识点，构建概念知识图谱，并通过随机游走抽样（random walk sampling）来生成符合特定主题和难度等级的数学题目。整个流程从数据提取、问题生成到后处理都已高度集成且可定制，方便快速扩展。

**主要特性：**

- **无缝集成 LLM：**  
  利用大型语言模型（LLM）自动从数学问题中提取主题和知识点，并生成新的数学题目。

- **异步并发请求支持：**  
  支持同时向 LLM API 发起多个请求，加速数据处理并提升处理规模。

- **自定义提示与元数据：**  
  可轻松配置提示模板、难度等级、题目类型以及其他元数据，以满足特定教学或研究需求。

- **知识图谱与随机游走采样：**  
  自动构建概念图谱，并使用随机游走算法从中选取相关知识点和主题，以生成聚焦性的数学问题。  
  *该部分算法严格复现以下论文提出的方法：*

  > Tang, Zhengyang, Xingxing Zhang, Benyou Wang, and Furu Wei. “Mathscale: Scaling instruction tuning for mathematical reasoning.” *arXiv preprint arXiv:2403.02884 (2024).*

- **模块化架构：**  
  明确的数据预处理、网络请求与响应后处理的分层设计，提高代码的可维护性和可扩展性。

---

## 项目结构

```
UltimateMath/
│
├── files/
│   ├── MATH.json              # 合并后的 MATH 数据集
│   ├── math_extraction.json   # 从 MATH 中提取的主题和知识点
│   └── math_generation.json   # 生成的数学问题和答案
│
├── handlers/
│   ├── data_extractor.py      # 后处理：从 LLM 响应中提取主题、知识点、题目、答案
│   └── data_preparator.py     # 前处理：构造发送给 LLM 的消息和元数据
│
├── network/
│   ├── payload_builder.py     # 构建发送给 LLM API 的 JSON 请求载荷
│   ├── request_manager.py     # 管理异步并发的 API 请求
│   └── response_handler.py    # 响应处理的装饰器与实用函数
│
├── utils/
│   └── graph_algorithm.py     # 构建概念图谱与执行随机游走采样
│
├── app.py                     # 主程序入口
├── config.py                  # 配置文件（API URL、模型、请求头、并发限制等）
└── prompt.py                  # 提示模板与问题类型、难度等级配置
```

---

## 核心流程

1. **准备数据集：**  
   起始数据为 MATH 数据集。根据需要合并 JSON 文件，确保将数据保存为 `files/MATH.json`。

2. **数据提取（主题与知识点）：**  
   使用 `data_preparator.py` 中的 `construct_math_extraction_messages` 生成可用于提取主题与知识点的提示信息。示例：
   ```python
   messages_list, metadata_list = construct_math_extraction_messages(
       file_path="files/MATH.json",
       required_fields={'question': 'problem', 'answer': 'solution', 'id': 'id'},
       num=100
   )
   ```
   然后调用：
   ```python
   import asyncio
   from handlers.data_extractor import extract_topics_and_knowledge_points
   from network.response_handler import retrieve_responses

   asyncio.run(retrieve_responses(messages_list, metadata_list, extract_topics_and_knowledge_points))
   ```
   提取结果会保存到 `files/math_extraction.json`。

3. **概念图谱构建与随机游走采样：**  
   使用 `utils/graph_algorithm.py` 中的 `build_concept_graph` 和 `random_walk_sampling` 从提取结果中构建概念图谱并执行随机游走抽样。  
   *该步骤严格复现了 Tang 等人（2024）的研究方法。*

4. **生成数学题目：**  
   使用 `construct_math_generation_messages` 为生成新的数学题构造提示信息，并向 LLM 发起请求：
   ```python
   messages_list, metadata_list = construct_math_generation_messages(num=100)
   ```
   然后运行：
   ```python
   from handlers.data_extractor import extract_question_and_answer
   asyncio.run(retrieve_responses(messages_list, metadata_list, extract_question_and_answer))
   ```
   新生成的数学题目及其答案将保存至 `files/math_generation.json`。

---

## 配置说明

**`config.py`**  
- **API_URL：** LLM 接口的请求地址  
- **HEADERS：** HTTP 请求头，包括鉴权令牌  
- **DEFAULT_PAYLOAD：** 默认请求参数（如模型名称）  
- **MAX_CONCURRENT_REQUESTS：** 控制并发请求的最大数量

根据实际环境和凭据修改 `config.py`。

---

## 提示模板与定制化

**`prompt.py`**  
- **MATH_EXTRACTION_PROMPT & MATH_GENERATION_PROMPT：**  
  用于指导 LLM 进行主题提取或题目生成的提示模板。
  
- **`question_types` & `difficulty_levels`：**  
  定义多种题目类型和难度等级，可根据需要添加、修改以生成不同类型的数学问题。

---

## 扩展与适配

- **数据预处理：**  
  如果需要适配新数据集或字段，修改或新增 `data_preparator.py` 中的函数。

- **数据后处理：**  
  若需提取更多信息或进行额外处理，可在 `data_extractor.py` 中添加或修改函数。

- **网络与请求载荷：**  
  如需更改目标 API 或模型，只需调整 `payload_builder.py` 和 `config.py` 中的设置。`request_manager.py` 与 `response_handler.py` 保证核心请求与响应流程不必修改。

---

## 引用

如使用本代码中概念图谱与随机游走采样的相关方法，请引用以下论文：

```
@article{tang2024mathscale,
  title={Mathscale: Scaling instruction tuning for mathematical reasoning},
  author={Tang, Zhengyang and Zhang, Xingxing and Wang, Benyou and Wei, Furu},
  journal={arXiv preprint arXiv:2403.02884},
  year={2024}
}
```

---

## 许可证

本项目以 [MIT License](LICENSE) 协议发布。您可在协议许可范围内自由使用、修改和分发本代码。

---

**UltimateMath** 简化并扩展了利用 LLM 进行数学问题生成、提取与处理的流程。通过集成已证实有效的概念图谱构建与随机游走采样策略，为研究人员与教育工作者提供生成高质量数学题目的灵活可扩展工具环境。