import os
import shutil
import logging
import pathlib as path

from osgeo import gdal
from osgeo_utils.samples import validate_cloud_optimized_geotiff as validate_cog
from s3fs import S3FileSystem
import rioxarray as rio 

JASMIN_API_URL = os.environ.get("JASMIN_API_URL")
JASMIN_TOKEN = os.environ.get("JASMIN_TOKEN")
JASMIN_SECRET = os.environ.get("JASMIN_SECRET")

logging.basicConfig(level=logging.INFO)

class EMODNETgenerationError(Exception):
    "Raised when the EMODNET file is nt processed"
    pass

def progress_callback(complete, message, cb_data:str = None) -> None:
    if int(complete*100) % 10 == 0:
        print(f"{complete*100:.0f}%", end="", flush=True)
    elif int(complete*100) % 3 == 0:
        print(".", end="", flush=True)

def process_edomnet(file, output_path):
    logging.info(f"Processing file...")
    output_path.mkdir(parents=True, exist_ok=True)
    output_tif_file = f'{output_path}/{file.stem}.tif'

    dataset_rio = rio.open_rasterio(str(file))
    dataset_rio["elevation"].rio.to_raster(output_tif_file)
    output_cog_file = f'{output_path}/{file.stem}_cog.tif'
    #input_file = gdal.Open(str(file))

    gdal.Translate(
       output_cog_file, 
       output_tif_file,
       format="COG",
       creationOptions=["COMPRESS=LZW", "BIGTIFF=YES"],
       callback=progress_callback
    )
    warnings, errors, _ = validate_cog.validate(output_cog_file, True, True)
    if warnings or errors:
        for w in warnings:
            print(w)
        for e in errors:
            print(e)
        return

    print("File generated OK")
    return output_cog_file

def merge_cogs(file_to_mosaic,output_file):
	gdal.Warp(output_file, file_to_mosaic, format="COG",
              options=["COMPRESS=LZW", "TILED=YES"])
	return output_file

def upload_jasmin(new_file, bucket, output_path):
    s3 = S3FileSystem(anon=False, key=JASMIN_TOKEN, secret=JASMIN_SECRET, client_kwargs={"endpoint_url": JASMIN_API_URL})
    file_name = path.Path(new_file).name
    remote_path = f"s3://{bucket}/{output_path}/{file_name}"
    with s3.open(remote_path, mode="wb", s3=dict(profile="default")) as remote_file:
        with open(new_file, mode="rb") as local_file:
            remote_file.write(local_file.read())

    print("upload done")

