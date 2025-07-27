import streamlit as st
import re
import google.generativeai as genai
from tools import get_weather
from build_prompt import build_mcp_prompt



#model context
system = "You are a helpful assistant that can answer questions and use tools when necessary."
tools = "get_weather(city): Gets weather using wttr.in. Call only when the query is about weather."

#session memory
if "memory" not in st.session_state:
    st.session_state.memory = []

st.set_page_config(page_title = "MCP Gemini Assistant", page_icon = "🌤️")
st.title("🌤️ MCP Gemini Assistant")
st.write("Ask anything -- especially about the weather")


#sidebar
st.sidebar.title("Document Search")
user_api_key = st.sidebar.text_input("Enter your Gemini API key", type="password")

model_options = [
    "gemini-1.5-pro",
    "gemini-1.5-flash",
    "gemini-1.0-pro",
    "gemini-1.0-pro-vision",
    "gemini-pro",
    "gemini-pro-vision",
    "gemini-2.0-flash-lite",

]
selected_model = st.sidebar.selectbox("Choose a Gemini Model", model_options, index=1)


if not user_api_key:
    st.sidebar.warning("Please enter your password to access the app.")
    st.stop()


try:
    genai.configure(api_key=user_api_key)
    model = genai.GenerativeModel(selected_model)

    # ✅ Validate the API key by making a minimal test request
    test_response = model.generate_content("Hello!")

    
    if hasattr(test_response, "text") and test_response.text:
        st.sidebar.success(f"✅ API key is valid. You can now use the app. The selected model is: {selected_model}")
    else:
        st.sidebar.error("❌ API key test failed. Please check your key.")
        st.stop()


except Exception as e:  
    st.sidebar.error(f"Error configuring API key: {e}")
    st.stop()





user_input = st.text_input("Enter your prompt:","")


def handle_tool_call(response):
    pattern = r"```tool_code\s*\nget_weather\(city=['\"](.*?)['\"]\)\s*```"

    match = re.search(pattern, response, re.DOTALL)

    if match:
        city = match.group(1).strip()
        st.info(f"[Tool] call detected for city: {city}")
        return get_weather(city)
    
    return None 

if user_input:
    prompt = build_mcp_prompt(system, tools, user_input,st.session_state.memory)
    response = model.generate_content(prompt).text
    tool_output = handle_tool_call(response)

    if tool_output:
        followup_prompt = (
            f"enter your prompt: {user_input}\n"
            f"tool_output: {tool_output}\n"
            f"respnd to the user naturally using this result\n"
        )   

        final_response = model.generate_content(followup_prompt).text
        st.session_state.memory.append(f"user: {user_input}") 
        st.session_state.memory.append(f"AI: {final_response}")
        st.success(final_response)
 

    else:
        st.session_state.memory.append(f"user:{user_input}")
        st.session_state.memory.append(f"AI:{response}")
        st.success(response)

#conversation history
with st.expander("memory"):
    for line in st.session_state.memory:
        st.markdown(f"-{line}")

#main loop
# if __name__ == "__main__":
#     while True:
#         user_input = input("enter your prompt: ")

#         if user_input.lower() in ["exit", "quit"]:
#             print("Exiting the program.")
#             break


#         prompt = build_mcp_prompt(system, tools, user_input, memory)
#         response = model.generate_content(prompt).text

#         tool_output = handle_tool_call(response)

#         if tool_output:
#             followup_prompt = (
#                 f"enter your prompt: {user_input}\n"
#                 f"Tool Output: {tool_output}\n"
#                 f"Respond to the user naturally using this result."
#             )

#             final_response = model.generate_content(followup_prompt).text

#             print(f"\nGemini Response: {final_response}")
#             memory.append(f"enter your prompt: {user_input}")  
#             memory.append(f"AI: {final_response}")

#         else:
#             print(f"\nGemini Response: {response}")
#             memory.append(f"enter your prompt: {user_input}")  
#             memory.append(f"AI: {response}")  