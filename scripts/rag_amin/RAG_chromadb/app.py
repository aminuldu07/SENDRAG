from shiny import App, ui, render
from query_openai import query_documents

app_ui = ui.page_fluid(
    ui.h2("PDF Q&A System (OpenAI)"),
    ui.input_text("question", "Ask a question:", placeholder="Type your question here..."),
    ui.input_action_button("ask_btn", "Get Answer"),
    ui.output_text("answer")
)

def server(input, output, session):
    @output
    @render.text
    def answer():
        if input.ask_btn():
            return query_documents(input.question())
        return "Ask a question to get started!"

app = App(app_ui, server)
