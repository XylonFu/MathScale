# UltimateMath 项目文档

## 项目概述

**UltimateMath** 是一个用于生成数学问题和答案的开发框架。通过处理 MATH 种子数据集，生成与大语言模型（LLM）交互所需的 `prompt`，最终生成新的数学问题及其对应的答案。该项目的核心在于利用 LLM 提取 MATH 种子数据集中的主题和知识点，构建知识图谱，并基于此图谱进行随机游走采样，生成新的数学问题。

**UltimateMath** 提供了一个灵活的框架，允许开发者基于现有的功能继续开发和扩展。该框架实现了异步并发处理请求和响应数据的功能，开发者无需关注网络请求的细节逻辑，只需专注于业务逻辑的实现，即数据的预处理与后处理。这显著减少了工作量，同时提高了项目的可维护性和可靠性。

## 项目结构

项目的目录结构如下：

```
UltimateMath/
│
├── files/
│   ├── GSM8K.parquet         # 存储原始的 MATH 数据集
│   ├── math_extraction.json  # 存储提取的主题和知识点数据
│   └── math_generation.json  # 存储生成的数学问题和答案数据
│
├── handlers/
│   ├── data_extractor.py     # 处理从响应中提取数据的代码（后处理）
│   └── data_preparator.py    # 处理消息构造的代码（预处理）
│
├── network/
│   ├── payload_builder.py    # 构建请求有效载荷的代码
│   ├── request_manager.py    # 管理并发请求的代码
│   └── response_handler.py   # 处理响应数据的装饰器和函数
│
├── utils/
│   └── graph_algorithm.py    # 构建知识图谱和随机游走采样的算法
│
├── app.py                    # 项目主程序入口
├── config.py                 # 配置文件，用于设置API请求的相关参数
└── prompt.py                 # 定义 prompt 模板及其相关配置
```

## 文件说明

### `app.py`

`app.py` 是项目的主程序入口。该文件负责调用 `data_preparator.py` 中的消息构造函数，并将生成的消息列表传递给 `response_handler.py` 中的 `retrieve_responses` 函数。随后，`data_extractor.py` 中的响应数据处理函数会处理从 LLM 返回的响应数据。以下是 `app.py` 的基本用法示例：

```python
messages_list, metadata_list = construct_math_generation_messages(num=100)
asyncio.run(retrieve_responses(messages_list, metadata_list, extract_question_and_answer))
```

通过这种方式，开发者可以轻松地生成数据，并根据需要进行扩展。当有新的业务需求时，只需在 `data_preparator.py` 或 `data_extractor.py` 中添加新的数据处理函数，无需修改网络逻辑部分的代码。

### `config.py`

`config.py` 文件包含了项目的配置项，包括 API 请求的地址、授权令牌、大语言模型的型号以及并发请求的最大数量。开发者可以在此文件中根据自己的需求调整配置。

### `prompt.py`

`prompt.py` 文件用于定义生成请求所需的 `prompt` 模板。该文件中包含了生成数学问题和提取主题知识点的模板，以及各种问题类型和难度级别的配置。

### `handlers/data_preparator.py`

`data_preparator.py` 文件负责数据的预处理。它包含了构造数学提取消息和生成数学问题消息的函数。根据指定的数量，这些函数会生成对应数量的消息列表和元数据。

### `handlers/data_extractor.py`

`data_extractor.py` 文件负责数据的后处理。它包含了从 LLM 响应中提取主题、知识点、问题和答案的函数。处理后的数据会存储在 `math_extraction.json` 和 `math_generation.json` 文件中。

### `network/payload_builder.py`

`payload_builder.py` 文件负责构建 API 请求的有效载荷。它根据传入的消息列表生成符合 API 要求的 JSON 结构。

### `network/request_manager.py`

`request_manager.py` 文件负责管理并发的 API 请求。它通过 `aiohttp` 库实现了异步请求的发送和响应的处理，并使用信号量限制同时进行的最大请求数。

### `network/response_handler.py`

`response_handler.py` 文件包含了处理 API 响应的装饰器和函数。装饰器 `process_response` 会提取响应中的数据并传递给处理函数。该文件还提供了 `retrieve_responses` 函数，用于批量处理消息并获取响应。

### `utils/graph_algorithm.py`

`graph_algorithm.py` 文件提供了构建知识图谱和在图谱上进行随机游走采样的算法。该算法用于生成与主题和知识点相关的数学问题。

## 使用说明

在使用这个框架时，开发者应关注以下几点：

1. **配置文件**：根据项目需求，在 `config.py` 中设置 API 请求地址、授权令牌和其他必要参数。
2. **预处理与后处理**：如果有新的数据处理需求，可以在 `handlers/data_preparator.py` 和 `handlers/data_extractor.py` 中添加新的函数，而无需修改网络逻辑部分的代码。
3. **prompt 模板**：在 `prompt.py` 中定义和调整生成 `prompt` 的模板，以适应不同的任务需求。
4. **运行项目**：执行 `app.py` 文件即可运行整个项目流程，生成并处理数学问题。

## 贡献指南

欢迎开发者贡献代码，改进和扩展 UltimateMath 项目。请确保在提交代码之前遵循项目的结构和风格，并测试您的代码以确保其功能正确。

## 许可证

此项目基于 [MIT 许可证](LICENSE) 开源，您可以自由使用、修改和分发代码。

---

通过这个开发框架，开发者可以方便地利用大语言模型生成新的数学问题。我们鼓励您深入了解代码，并根据自己的需求进行定制和扩展。
