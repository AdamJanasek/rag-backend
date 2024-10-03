async def save_file(file):
    file_path = f'uploaded_files/{file.name}'
    with open(file_path, 'wb') as f:
        f.write(file.body)
    return file_path


def validate_files(files):
    if not files:
        raise ValueError('No files provided.')
