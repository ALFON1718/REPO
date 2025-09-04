import os
import dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.prompt import Prompt

dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
console = Console()

def main():
    # Mensaje de bienvenida con rich
    welcome_text = Text("🤖 Stateful Chatbot", style="bold blue")
    welcome_text.append("\nCompletions API - Escribe 'exit' para salir", style="dim")
    console.print(Panel(welcome_text, title="Chatbot", border_style="blue"))
    
    model = "gpt-4o-mini"
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    while True:
        user_input = Prompt.ask("[bold green]Tú[/bold green]")
        if user_input.lower() in {"exit", "quit"}:
            # Mostrar contexto al salir
            context_text = Text("Historial de conversación:", style="bold yellow")
            for i, msg in enumerate(conversation, 1):
                role = msg.get("role", "").capitalize()
                content = msg.get("content", "")
                if role == "System":
                    context_text.append(f"\n[{i}] [bold cyan]{role}:[/bold cyan] {content}", style="dim")
                elif role == "User":
                    context_text.append(f"\n[{i}] [bold green]{role}:[/bold green] {content}")
                else:
                    context_text.append(f"\n[{i}] [bold blue]{role}:[/bold blue] {content}")
            
            console.print(Panel(context_text, title="📋 Contexto Completo", border_style="yellow"))
            break
            
        if "context" in user_input.lower():
            # Mostrar contexto cuando se solicite
            context_text = Text("Historial de conversación:", style="bold yellow")
            for i, msg in enumerate(conversation, 1):
                role = msg.get("role", "").capitalize()
                content = msg.get("content", "")
                if role == "System":
                    context_text.append(f"\n[{i}] [bold cyan]{role}:[/bold cyan] {content}", style="dim")
                elif role == "User":
                    context_text.append(f"\n[{i}] [bold green]{role}:[/bold green] {content}")
                else:
                    context_text.append(f"\n[{i}] [bold blue]{role}:[/bold blue] {content}")
            
            console.print(Panel(context_text, title="📋 Contexto Completo", border_style="yellow"))
            continue
        conversation.append({"role": "user", "content": user_input})
        try:
            response = client.chat.completions.create(
                model=model,
                messages=conversation
            )
            text = response.choices[0].message.content.strip()
            # Mostrar respuesta del bot con rich
            bot_panel = Panel(
                text,
                title="[bold blue]🤖 Bot[/bold blue]",
                border_style="blue",
                padding=(1, 2)
            )
            console.print(bot_panel)
            conversation.append({"role": "assistant", "content": text})
        except Exception as e:
            # Mostrar errores con rich
            error_panel = Panel(
                str(e),
                title="[bold red]❌ Error[/bold red]",
                border_style="red",
                padding=(1, 2)
            )
            console.print(error_panel)

if __name__ == "__main__":
    main()
