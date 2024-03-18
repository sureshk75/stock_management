$to_del = "__pycache__", "build", "dist", "stck_invt.spec"
foreach ($item in $to_del)
{
    Remove-Item $item -Force -Recurse -ErrorAction SiletlyContinue
}
pyinstaller --onefile --windowed --add-data "resource/*;resource" --name "stck_invt" --icon=resource/icon.ico --version-file="file_version_info.txt" controller.py