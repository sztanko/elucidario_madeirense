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


@app.command()
def ocrfix():
    """Phase 3a: deterministic OCR fixes (data/03_clean)."""
    from elucidario.stages import ocrfix as stage

    typer.echo(json.dumps(stage.run(), indent=2, ensure_ascii=False))


@app.command()
def ocrproof(
    step: str = typer.Argument(..., help="prepare | submit | wait | collect"),
    budget: float = typer.Option(15.0, help="USD cap for submission"),
    only: int = typer.Option(0, help="submit only N evenly spaced chunks (pilot)"),
):
    """Phase 3b: LLM proofreading via the Batch API."""
    from elucidario.llm.batch import BatchJob
    from elucidario.stages import ocrproof as stage

    if step == "prepare":
        out = stage.prepare()
    elif step == "submit":
        out = stage.submit(budget, only or None)
    elif step == "wait":
        BatchJob("ocr_proof").wait()
        out = {"done": True}
    else:
        out = stage.collect()
    typer.echo(json.dumps(out, indent=2, ensure_ascii=False))


@app.command()
def structure():
    """Phase 4a: articles -> typed blocks (data/04_structured)."""
    from elucidario.stages import structure as stage

    typer.echo(json.dumps(stage.run(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    app()
