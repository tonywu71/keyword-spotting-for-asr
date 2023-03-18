import typer

from pathlib import Path

from kws.morph_decomposition.query_to_morph import apply_morph_to_queries_file


def main(queries_filepath: str,
         morph_filepath: str,
         output_filename: str):
    """
    Apply morphological transformations to a Queries file. The output path
    is saved in the same directory as the input Queries file.
    """
    
    output_dir = Path(queries_filepath).parent
    output_filepath = output_dir / output_filename
    
    apply_morph_to_queries_file(queries_filepath=queries_filepath,
                                morph_filepath=morph_filepath,
                                output_filepath=str(output_filepath))
    
    print(f"Output succesfully written to {output_filepath}")
    
    return


if __name__ == "__main__":
    typer.run(main)
