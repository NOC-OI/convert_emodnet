#!/bin/bash

mkdir emodnet
cd emodnet
# download the E3 tile
wget https://downloads.emodnet-bathymetry.eu/v11/E3_2022.nc.zip 
unzip E3_2022.nc.zip

# download the E4 tile
wget https://downloads.emodnet-bathymetry.eu/v11/E4_2022.nc.zip
unzip E4_2022.nc.zip

rm E4_2022.nc.zip E3_2022.nc.zip

cd ..

conda env update -f environment.yml
source activate imfe_convert_emodnet

python process_emodnet -i emodnet -o . --skip-upload

