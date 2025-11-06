
import typer
from frontmatters.commands import add_description, tree, organize, filter

app = typer.Typer()
app.add_typer(add_description.app, name="description")
app.add_typer(tree.app, name="tree")
app.add_typer(organize.app, name="organize")
app.add_typer(filter.app, name="filter")

if __name__ == "__main__":
    app()
