import click
from pathlib import Path
from process_emodnet import EMODNETgenerationError,process_edomnet,upload_jasmine, merge_cogs
import shutil
import os



JASMIN_API_URL = os.environ.get("JASMIN_API_URL")
JASMIN_TOKEN = os.environ.get("JASMIN_TOKEN")
JASMIN_SECRET = os.environ.get("JASMIN_SECRET")

OUTPUT_FILE="EMODNet_2020.tif"


@click.command()
@click.option("-i", "--input", required=True, help="Directory containing unprocessed EMODNET nc files")
@click.option("-o", "--output", required=True, help="Directory to output the optimised files")
@click.option("-b", "--bucket", required=False, help="Name of the bucket to upload to")
@click.option("--skip-upload", "skip_upload", is_flag=True, default=False, help="Generate COG files only without uploading")
def main(input: str, output: str, bucket: str, skip_upload: bool):
    if not skip_upload:
        if not bucket:
            click.echo("Bucket name must be specified with --bucket if uploading. Else set --skip-upload to not upload to the cloud.")
            return

    input_path = Path(input)
    output_path = Path(output)
    files = list(input_path.glob("**/*.nc"))
    click.echo(f"{len(files)} files to process")
    input_cog_files = []
    for file in Path(input).glob('*.nc'):
        try:
            # Process the file to COG format
            input_cog_files.append(process_edomnet(file, output_path))
            
        except EMODNETgenerationError:
            print("Exception Occurred:EDOMNet files not processed")

    new_file_path = merge_cogs(input_cog_files,f'{output_path}/{OUTPUT_FILE}')

    if not skip_upload:
        try:
            # Upload to cloud storage
            upload_jasmine(new_file_path, bucket, output_path)
        except EMODNETgenerationError:
            print("Exception Occurred:EDOMNet files not uploaded to JASMIN")

    if not skip_upload:
    # Remove intermediate directory
        shutil.rmtree(Path(output_path))

if __name__ == "__main__":
    main()