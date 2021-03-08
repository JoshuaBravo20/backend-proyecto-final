def img_type_file(filename, extensions):
    return '.' in filename.rsplit('.', 1)[1].lower() in extensions
