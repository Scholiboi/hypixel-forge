import hashlib
import os
import sys
import time

def calculate_hash(file_path, algorithm="sha256"):
    """Calculate hash of a file using the specified algorithm."""
    hash_funcs = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256
    }
    
    if algorithm not in hash_funcs:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
        
    hash_obj = hash_funcs[algorithm]()
    
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash_obj.update(byte_block)
    
    return hash_obj.hexdigest()

def generate_checksums(exe_path, output_file="checksums.txt", version="1.1.2"):
    """Generate a checksums verification file for the executable."""
    
    if not os.path.exists(exe_path):
        return f"Error: File '{exe_path}' not found."
    
    try:
        file_name = os.path.basename(exe_path)
        file_size = os.path.getsize(exe_path)
        
        md5_hash = calculate_hash(exe_path, "md5")
        sha1_hash = calculate_hash(exe_path, "sha1")
        sha256_hash = calculate_hash(exe_path, "sha256")

        with open(output_file, "w") as f:
            f.write(f"Hypixel Dwarven Forge v{version} - Checksum Verification\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-" * 60 + "\n\n")
            
            f.write(f"File: {file_name}\n")
            f.write(f"Size: {file_size:,} bytes\n\n")
            
            f.write("CHECKSUMS:\n")
            f.write(f"MD5:     {md5_hash}\n")
            f.write(f"SHA1:    {sha1_hash}\n")
            f.write(f"SHA256:  {sha256_hash}\n\n")
            
            f.write("VERIFICATION INSTRUCTIONS:\n")
            f.write("To verify file integrity, compare the checksums above with those\n")
            f.write("generated from your downloaded file using one of these methods:\n\n")
            
            f.write("Windows (PowerShell):\n")
            f.write(f"  Get-FileHash -Algorithm SHA256 {file_name}\n\n")
            
            f.write("Windows (Command Prompt):\n")
            f.write(f"  certUtil -hashfile {file_name} SHA256\n\n")
            
            f.write("Linux/macOS:\n")
            f.write(f"  sha256sum {file_name}\n")
        
        return f"Checksum verification file created: {output_file}"
    
    except Exception as e:
        return f"Error generating checksums: {str(e)}"

default_exe = "./dist/hypixel_dwarven_forge-v1.1.2.exe"

result = generate_checksums(default_exe)
print(result)