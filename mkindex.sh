#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <compressed_file>"
    exit 1
fi

# Store the provided compressed file path
compressed_file="$1"
# Create a temporary directory for extracting the contents of the compressed file
temp_dir=$(mktemp -d)

echo "Uncompressing file..."

# Check the type of compressed file and extract its contents to the temporary directory
if [[ "$compressed_file" == *.zip ]]; then
    unzip "$compressed_file" -d "$temp_dir" > /dev/null 2>&1
elif [[ "$compressed_file" == *.rar ]]; then
    unrar x -o+ "$compressed_file" "$temp_dir" > /dev/null 2>&1
else
    echo "Unsupported compressed file format"
    exit 1
fi

echo "Creating index files..."

# Generate a unique string for the index directory name
unique_string=""
base_name=$(basename "$compressed_file")
index_base_name="${base_name%.*}"  # Remove extension
index_dir_parent=$(dirname "$compressed_file")

# Check if an index directory with the same name already exists
while [ -d "$index_dir_parent/${index_base_name}${unique_string}.index" ]; do
    unique_string+="_"
done

# Create the final index directory path
index_dir="${index_dir_parent}/${index_base_name}${unique_string}.index"
# Create the index directory
mkdir -p "$index_dir"

# Iterate over each file and directory in the temporary extraction directory
while IFS= read -r -d '' entry; do
    # Get the timestamp of the file or directory
    timestamp=$(stat -c %Y "$entry")
    # Generate the path for the new entry in the index directory
    new_path=${entry/$temp_dir/$index_dir}
    
    # Check if the entry is a directory and create it in the index directory
    if [ -d "$entry" ]; then
        mkdir -p "$new_path"
    # Check if the entry is a file and create an empty file with the corresponding timestamp
    elif [ -f "$entry" ]; then
        touch -d "@$timestamp" "$new_path"
    fi
done < <(find "$temp_dir" -print0)

# Display a message indicating the successful creation of the index
echo "Index created at: $index_dir"

# Clean up the temporary directory
rm -r "$temp_dir"
