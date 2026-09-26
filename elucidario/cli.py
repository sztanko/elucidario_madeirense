import json

import typer

app = typer.Typer(no_args_is_help=True, help="Elucidário Madeirense pipeline")


@app.callback()
def main():
    """Run a pipeline stage."""


@app.command()
def extract():
    """Phase 1: PDF -> logical lines (data/01_layout)."""
    from elucidario.stages import extract as stage

    typer.echo(json.dumps(stage.run(), indent=2, ensure_ascii=False))


@app.command()
def segment():
    """Phase 2: lines -> articles (data/02_segments)."""
    from elucidario.stages import segment as stage

    typer.echo(json.dumps(stage.run(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    app()
