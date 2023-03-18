import typer

from pathlib import Path

from kws.morph_decomposition.ctm_to_morph import apply_morph_to_ctm_file


def main(ctm_filepath: str,
         morph_filepath: str,
         output_filename: str):
    """
    Apply morphological transformations to a CTM file. The output path
    is saved in the same directory as the input CTM file.
    """
    
    output_dir = Path(ctm_filepath).parent
    output_filepath = output_dir / output_filename
    
    apply_morph_to_ctm_file(ctm_filepath=ctm_filepath,
                            morph_filepath=morph_filepath,
                            output_filepath=str(output_filepath))
    
    print(f"Output succesfully written to {output_filepath}")
    
    return


if __name__ == "__main__":
    typer.run(main)
