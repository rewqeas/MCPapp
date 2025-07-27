def build_mcp_prompt(system, tools, query, memory=[]):
    prompt = ""

    prompt += f"System: {system}\n\n"
    prompt += f"Available Tools:\n{tools}\n\n"

    if memory:
        prompt += "Memory:\n" + "\n".join(memory) + "\n\n"

    prompt += f"Query:\n{query}\n\n"

    prompt += (
        "Instructions:\n"
        "1. If the query is about weather, respond only with a code block like this:\n"
        "```tool_code\nget_weather(city='CityName')\n```\n"
        "2. If the query is about exchange rates, respond only with a code block like this:\n"
        "```tool_code\nget_exchange_rate(from_currency='FromCurrency', to_currency='ToCurrency')\n```\n"
        "3. If the query is about jokes, sarcasm, or vulgar humor, respond only with a code block like this:\n"
        "```tool_code\nget_jokes(category='Any', allow_vulgar=True)\n```\n"
        "Otherwise, reply normally.\n"
    )

    return prompt
