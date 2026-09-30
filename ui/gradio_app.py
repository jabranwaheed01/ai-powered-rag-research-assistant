import gradio as gr
from app.services.chatbot_service import ChatbotService

bot = ChatbotService()

def ask_question(question, topic, year, mode):

    if not question.strip():
        return "Please enter a question.", ""

    try:
        year = int(year) if year else None

        result = bot.ask(
            query=question,
            top_k=5,
            topic=topic if topic else None,
            year=year,
            mode=mode
        )

        answer = result["answer"]
        sources = result["sources"]

        print("DEBUG SOURCES:", sources)

        source_lines = []

        for i, source in enumerate(sources):
            source_year = source.get("year", "N/A")

            if isinstance(source_year, float):
                source_year = int(source_year)

            source_lines.append(
                f"{i + 1}. {source.get('document', 'N/A')}\n"
                f"   Topic: {source.get('topic', 'N/A')}\n"
                f"   Year: {source_year}"
            )

        source_text = "\n\n".join(source_lines)

        return answer, source_text

    except Exception as e:
        return f"Error: {str(e)}", ""


demo = gr.Interface(
    fn=ask_question,
    inputs=[
        gr.Textbox(
            label="Ask a Question",
            placeholder="Ask something about climate change..."
        ),
        gr.Dropdown(
            choices=["", "environment", "health", "economy"],
            label="Topic",
            value=""
        ),
        gr.Dropdown(
            choices=["", "2023"],
            label="Year",
            value=""
        ),
        gr.Dropdown(
            choices=["qa", "summary"],
            label="Mode",
            value="qa"
        )
    ],
    outputs=[
        gr.Textbox(label="Answer"),
        gr.Textbox(label="Sources")
    ],
    title="AI-Powered RAG Research Assistant",
    description="Ask questions from the indexed research documents."
)


demo.launch(share=True)

