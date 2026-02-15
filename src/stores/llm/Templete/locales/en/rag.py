from string import Template

##   System_Prompt  ##

System_Prompt = Template("\n".join([
    "You are a smart general-purpose assistant capable of understanding any English text.",
    "Extract the most relevant information from the provided content.",
    "Rank the results based on their importance relative to the question.",
    "Provide clear and concise answers to the user.",
    "Answer in the same language as the question."
]))

Document_Prompt = Template("\n".join([
    "## Document Number: $doc_num ##",
    "### Content: $chunk_text",
]))

Footer_Prompt = Template("\n".join([
    "Focus on answering in the same language as the query.",
    "Do not repeat information.",
    "Show only the best results relevant to the user's question.",
    "If no direct answer is found, provide the best suggestion based on the content.",
    "## Answer"
]))
