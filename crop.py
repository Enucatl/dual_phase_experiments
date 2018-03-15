import click
import h5py
import numpy as np


@click.command()
@click.argument("input_filename", type=click.Path(exists=True))
@click.argument("output_filename", type=click.Path())
@click.option("--roi", nargs=4, type=int)
def main(input_filename, output_filename, roi):
    with h5py.File(input_filename, "r") as input_file:
        min_x, max_x, min_y, max_y = roi
        dpc_reconstruction = input_file["postprocessing/dpc_reconstruction"]
        dark_field = dpc_reconstruction[min_y:max_y, min_x:max_x, 2]
        absorption = dpc_reconstruction[min_y:max_y, min_x:max_x, 0]
        with h5py.File(output_filename) as output_file:
            group = output_file.require_group("postprocessing")
            if "dark_field" in group:
                del group["dark_field"]
            group.create_dataset("dark_field", data=dark_field)
            if "ratio" in group:
                del group["ratio"]
            ratio = np.log(dark_field) / np.log(absorption)
            ratio[absorption > 0.8] = 0
            group.create_dataset("ratio", data=ratio)


if __name__ == "__main__":
    main()
