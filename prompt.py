MATH_EXTRACTION_PROMPT = (
    "Please analyze the following math problem and extract the topics and knowledge points involved. "
    "Output the result in JSON format as follows:\n"
    "{{\n"
    "  \"topics\": [\"Topic1\", \"Topic2\"],\n"
    "  \"knowledge_points\": [\"Point1\", \"Point2\", \"Point3\"]\n"
    "}}\n\n"
    "Problem: {question}"
)

MATH_GENERATION_PROMPT = (
    "As a math professor, create a {question_type} question at the {difficulty} level. "
    "{type_description} {difficulty_description} "
    "Ensure that the question you create is strictly aligned with the specified type, difficulty level, topics, and knowledge points. "
    "It should effectively challenge the intended audience and require the appropriate application of the provided topics and knowledge points.\n\n"
    "Base the question on the following topics and knowledge points.\n\n"
    "Topics:\n{topics}\n\nKnowledge Points:\n{knowledge_points}\n\n"
    "Please structure your response as follows:\n"
    "Question: <Generated Question>\n"
    "Answer: <Generated Answer>"
)

question_types = {
    "Problem-Solving": "Create a problem that requires logical reasoning or computational steps to solve.",
    "Proof": "Formulate a mathematical statement that demands a rigorous proof, ensuring it is complex and detailed.",
    "Inductive Reasoning": "Provide a sequence or set of examples that lead to the identification of an underlying pattern or general rule.",
    "Analytical Reasoning": "Present a complex problem that must be broken down into smaller components for detailed analysis.",
    "Construction": "Design a task focused on constructing a specific mathematical object, such as a geometric figure or algebraic expression, with clear conditions.",
    "Open-Ended": "Pose a question that allows for multiple valid approaches or solutions, encouraging deep and creative thinking.",
    "Counterexample": "Present a statement or assumption that requires the identification of a counterexample to disprove it.",
    "Comparison and Contrast": "Create a problem that centers on comparing and contrasting different mathematical objects, methods, or theories."
}

difficulty_levels = {
    "Elementary School": "The question should be straightforward, focusing on fundamental concepts suitable for young learners.",
    "Middle School": "The question should focus on basic concepts, requiring clear logical reasoning and application of introductory principles.",
    "High School": "The question should be moderately challenging, requiring the application of more complex reasoning and multi-step problem-solving.",
    "Undergraduate": "The question should be challenging, requiring deep understanding and the application of advanced concepts.",
    "Master's": "The question should be advanced, demanding critical thinking and the ability to engage deeply with specialized topics.",
    "PhD": "The question should be highly advanced, possibly exploring new ideas or requiring original approaches and deep theoretical insight."
}
