import typer


def combine_systems() -> None:
    """Combine two systems into one"""
    typer.echo("Combining systems")


if __name__ == "__main__":
    typer.run(combine_systems)
