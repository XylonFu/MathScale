# MathScale

**MathScale** 是一个开发框架，用于利用大型语言模型（LLMs）生成、提取和处理数学问题。框架从种子数据集（MATH）入手，提取主题、知识点及相关概念，构建概念图谱，并通过随机游走抽样生成新的数学问题和解决方案。整个流程——从数据提取、问题生成到后处理——高度集成且支持自定义，为研究人员、教育工作者和开发人员提供了便捷的扩展基础。

**主要特点：**

- **基于 LLM 的数据提取与生成：**  
  利用 LLM 自动从 MATH 数据集中提取主题和知识点，生成与指定主题、难度和问题类型一致的新数学问题。

- **异步并发，支持大规模扩展：**  
  通过异步操作处理多个 LLM 请求，支持大规模数据处理并减少处理时间。

- **可自定义的提示与元数据：**  
  细化提示模板、难度级别、问题类型等配置。根据具体目标（如教学、研究或评估）生成定制化的任务。

- **概念图谱构建与随机游走采样（MathScale 方法）：**  
  构建提取概念的知识图谱，并通过随机游走采样识别互相关联的主题和知识点。  
  *该方法严格复现了 MathScale 论文中描述的算法：*

  > Tang, Zhengyang, Xingxing Zhang, Benyou Wang, and Furu Wei.  
  > 《Mathscale: Scaling instruction tuning for mathematical reasoning》  
  > *arXiv preprint arXiv:2403.02884 (2024)*

- **模块化与可扩展架构：**  
  数据预处理、请求处理、响应后处理各部分模块化分离，便于与其他数据集、API 或 LLM 服务集成。无需修改网络逻辑即可调整提示、处理步骤和输出。

---

## 项目结构

```
MathScale/
│
├── files/
│   ├── MATH.json              # 合并后的 MATH 数据集
│   ├── math_extraction.json   # 提取的主题与知识点
│   └── math_generation.json   # 生成的数学问题及解决方案
│
├── handlers/
│   ├── data_extractor.py      # 响应后处理：从 LLM 响应中提取数据
│   └── data_preparator.py     # 请求预处理：构造 LLM 请求的提示和元数据
│
├── network/
│   ├── payload_builder.py     # 构建 LLM API 的 JSON 请求载荷
│   ├── request_manager.py     # 管理异步并发的 API 请求
│   └── response_handler.py    # 处理 LLM 响应的装饰器与函数
│
├── utils/
│   └── graph_algorithm.py     # 构建概念图谱并执行随机游走采样
│
├── app.py                     # 主程序入口
├── config.py                  # 配置文件（API URL、请求头、模型、并发限制）
└── prompt.py                  # 提示模板、问题类型与难度级别
```

---

## 快速开始

### 1. 准备 MATH 数据集

1. 将 MATH 数据集的 JSON 文件放置或合并到 `files/MATH.json` 下。
2. 根据需要调整代码中的 `input_directory` 和 `output_file_path`。

### 2. 提取主题与知识点

**目标：** 从 `MATH.json` 中的数学问题提取主题和知识点。

```python
from handlers.data_preparator import construct_math_extraction_messages
from handlers.data_extractor import extract_topics_and_knowledge_points
from network.response_handler import retrieve_responses
import asyncio

# 准备提取请求
messages_list, metadata_list = construct_math_extraction_messages(
    file_path="files/MATH.json",
    required_fields={'question': 'problem', 'answer': 'solution', 'id': 'id'},
    num=100
)

# 通过 LLM 运行提取过程
asyncio.run(retrieve_responses(messages_list, metadata_list, extract_topics_and_knowledge_points))
```

运行完成后，提取结果将保存在 `files/math_extraction.json` 中。

### 3. 构建概念图谱与随机游走采样

**目标：** 基于提取的数据构建概念图谱，并通过随机游走采样识别互相关联的主题与知识点。  
生成新问题时，该步骤会自动运行，代码内部调用 `utils/graph_algorithm.py` 中的 `build_concept_graph` 和 `random_walk_sampling`。

### 4. 生成新数学问题

**目标：** 生成符合选定难度级别、问题类型及提取主题与知识点的新数学问题。

```python
from handlers.data_preparator import construct_math_generation_messages
from handlers.data_extractor import extract_question_and_answer

# 准备生成请求
messages_list, metadata_list = construct_math_generation_messages(num=100)

# 通过 LLM 运行生成过程
asyncio.run(retrieve_responses(messages_list, metadata_list, extract_question_and_answer))
```

生成的数学问题及其答案将保存在 `files/math_generation.json` 中。

---

## 配置

**`config.py`** 提供核心配置：

- **API_URL：** LLM 服务的接口地址。
- **HEADERS：** 如果需要鉴权，包含认证令牌。
- **DEFAULT_PAYLOAD：** 指定使用的 LLM 模型及默认参数。
- **MAX_CONCURRENT_REQUESTS：** 控制大规模批量处理的并发请求数。

根据环境和使用的 LLM 服务调整这些参数。

---

## 自定义

**`prompt.py`** 支持生成和提取过程的自定义：

- **MATH_EXTRACTION_PROMPT & MATH_GENERATION_PROMPT：**  
  预定义的提示模板，用于指导 LLM 提取主题或生成问题/答案。
  
- **`question_types` & `difficulty_levels`：**  
  定义多种问题类型（如“问题求解”“证明”）和难度级别（如“小学”“博士”）。根据教学或研究目标扩展或修改这些配置。

---

## 扩展框架

- **数据预处理：**  
  针对新数据集或格式，修改 `data_preparator.py` 以生成合适的提示和元数据。

- **数据后处理：**  
  如果需要更复杂的解析或附加元数据字段，可编辑 `data_extractor.py` 调整 LLM 响应的提取逻辑。

- **网络与请求载荷适配：**  
  如果切换到其他 LLM 提供商或模型，可调整 `payload_builder.py` 和 `config.py`。核心的请求与响应逻辑无需更改。

---

## 引用

如果您在代码中使用了概念图谱与随机游走采样方法，请引用 MathScale 论文：

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

本项目基于 [MIT License](LICENSE) 协议开源。您可以按照许可证的条款自由使用、修改和分发代码。

---

**MathScale** 简化了基于 LLM 的数学问题生成流程。通过整合 MathScale 方法中的概念图谱与随机游走采样，为教育工作者、研究人员和开发者提供了一个强大、可扩展的数学内容生成平台。