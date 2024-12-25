#!/bin/bash

# Instructions:
# 1. This script downloads specified files from the Hailo Model Zoo.
# 2. The files will be saved into the 'resources' directory.
# 3. Ensure 'wget' is installed on your system.

# Array of file URLs to download
FILE_URLS=(
    "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hackathon/ahhahha.mp3"
    "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hackathon/brandyyyyyy.mp3"
    "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hackathon/foya.mp3"
    "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hackathon/mosko_barking.mp3"
    "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hackathon/No.mp3"
    "https://hailo-csdata.s3.eu-west-2.amazonaws.com/resources/hackathon/Tovaaaaa.mp3"
)

# Create resources directory if it doesn't exist
mkdir -p ./resources

# Function to download a file
download_file() {
    URL=$1
    FILENAME=$(basename "$URL")
    OUTPUT_FILE="./resources/$FILENAME"

    echo "Downloading: $FILENAME"

    # Download the file
    wget --quiet --show-progress --no-clobber --directory-prefix=./resources "$URL" || {
        echo "Error downloading: $URL"
        return 1
    }

    echo "Successfully downloaded: $FILENAME"
}

# Main logic
echo "Starting downloads..."

# Iterate over the list of URLs and download each
for URL in "${FILE_URLS[@]}"; do
    download_file "$URL"
done

echo "Clone Dynamixel SDK"
mkdir -p ./open_source
pushd "open_source"
git clone https://github.com/ROBOTIS-GIT/DynamixelSDK.git
pushd "DynamixelSDK/python"
sudo python setup.py install
popd
popd


echo "All downloads completed."
