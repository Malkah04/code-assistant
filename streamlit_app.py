
import streamlit as st

from classify_request import classify
from explain import explain_code
from generation.pipeline import generate_code
from generation.feedback import save_user_solution
from memory import (
    init_memory,
    save_interaction,
    get_last_k_message,
)


st.set_page_config(
    page_title="AI Coding Assistant",
    layout="wide",
)

st.title("AI Coding Assistant")
st.caption(
    "Generate code, explain programming concepts, "
    "and continue previous conversations."
)

init_memory()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "reference_question" not in st.session_state:
    st.session_state.reference_question = ""

if "reference_solution" not in st.session_state:
    st.session_state.reference_solution = ""


with st.sidebar:
    st.header("Settings")

    st.write("**Available modes**")
    st.markdown("- Code generation")
    st.markdown("- Code explanation")
    st.markdown("- Conversation memory")
    st.markdown("- User-provided reference solutions")

    st.divider()

    if st.button("Clear visible chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption(
        "Clearing the visible chat does not delete saved database history."
    )


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


with st.expander("Add a Reference Solution", expanded=False):
    if st.session_state.messages:
        latest_question = next(
            (
                message["content"]
                for message in reversed(st.session_state.messages)
                if message["role"] == "user"
            ),
            "",
        )
        if not st.session_state.reference_question:
            st.session_state.reference_question = latest_question

    with st.form("save_reference_form"):
        reference_question = st.text_area(
            "Programming question",
            key="reference_question",
            placeholder="Write the original programming question",
            height=100,
        )

        solution = st.text_area(
            "Reference solution",
            key="reference_solution",
            placeholder=(
                "def is_even(n):\n"
                "    return n % 2 == 0"
            ),
            height=200,
        )

        submitted = st.form_submit_button("Save as Reference")

        if submitted:
            try:
                result = save_user_solution(
                    question=reference_question,
                    solution=solution,
                )

                st.success(result)

                st.session_state.reference_question = ""
                st.session_state.reference_solution = ""

            except ValueError as error:
                st.error(str(error))

            except Exception as error:
                st.error(f"Could not save solution: {error}")
                print(f"Error saving reference solution: {error}")


question = st.chat_input("Ask a programming question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                memory_context = get_last_k_message(5)
                intent = classify(question)

                if intent == "EXPLAIN":
                    response = explain_code(
                        query=question,
                        memory=memory_context,
                    )

                elif intent == "GENERATE":
                    response = generate_code(
                        question=question,
                        memory=memory_context,
                    )

                else:
                    response = (
                        "I couldn't determine your request type. "
                        "Please try rephrasing your question."
                    )

                st.markdown(response)

                save_interaction(
                    user_message=question,
                    intent=intent,
                    assistant_response=response,
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                })

            except Exception as error:
                st.error(
                    "Something went wrong while processing your request. "
                    "Check the terminal for details."
                )
                print(f"Error processing request: {error}")
