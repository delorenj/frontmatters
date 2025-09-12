
import typer
from frontmatters.commands import add_description, tree, organize

app = typer.Typer()
app.add_typer(add_description.app, name="description")
app.add_typer(tree.app, name="tree")
app.add_typer(organize.app, name="organize")

if __name__ == "__main__":
    app()
