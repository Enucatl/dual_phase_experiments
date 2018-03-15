import click
import h5py
import numpy as np


@click.command()
@click.argument("input_filenames", nargs=-1, type=click.Path(exists=True))
@click.argument("output_filename", type=click.Path())
def main(input_filenames, output_filename):
    with h5py.File(output_filename) as output_file:
        for i, input_filename in enumerate(input_filenames):
            with h5py.File(input_filename, "r") as input_file:
                dark_field = input_file["postprocessing/dark_field"]
                output_file["dark_field_{:02}".format(i)] = h5py.ExternalLink(
                    input_filename,
                    "postprocessing/dark_field")
                ratio = input_file["postprocessing/ratio"]
                output_file["ratio_{:02}".format(i)] = h5py.ExternalLink(
                    input_filename,
                    "postprocessing/ratio")

if __name__ == "__main__":
    main()
