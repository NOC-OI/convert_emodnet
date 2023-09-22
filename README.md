# Converting Emodnet

This script takes the GEBCO NetCDF file (~7GB) and converts to a cloud optimised GeoTiff, validates the new file, and uploads to JASMIN.

---


## Prerequisites
Before running the script you will need the following environment variables set:
- JASMIN_TOKEN
- JASMIN_SECRET
- JASMIN_API_URL

INPUT_PATH, OUTPUT_PATH & BUCKET_NAME within the script will likely need changing too.


## Running the Script
To run script, run the folowing commands:
``` shell
conda env update -f environment.yml
conda activate imfe_convert_gebco

python process_emodnet -i  input_dir -o output_dir -b bucket name
```

  - input_dir should be replaced with the path to directory containing the .nc file of data.
  - output_dir should be replaced with the path to directory containing the COG file.
  - bucket_name is the name of the bucket in JASMIN to write to

### Running the Script without Uploading
To generate the STAC catalog without uploading use the command: `python process_emodnet -i  input_dir -o output_dir -b bucket name --skip-upload`.