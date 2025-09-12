
import typer
from frontmatters.commands import add_description

app = typer.Typer()
app.add_typer(add_description.app, name="description")

if __name__ == "__main__":
    app()
