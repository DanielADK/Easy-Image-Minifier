def formatFileSize(size):
    factor = 1024
    unit = ""
    for u in ["", "kB", "MB", "GB", "TB"]:
        if size < factor:
            unit = u
            break
        size /= factor
    return f"{size:.1f} {unit}"


def compressMe(file, quality, verbose=False):
    oldsize = os.stat(file).st_size
    newfile = file.split(".")
    min_file = ".".join(newfile[0:-1]) + ".min." + newfile[-1]
    picture = Image.open(file)
    picture.save(min_file, "JPEG", optimize=True, quality=quality)

    newsize = os.stat(min_file).st_size
    percent = round((oldsize - newsize) / float(oldsize) * 100)
    if verbose:
        print("Compression: {2}%".format(oldsize, newsize, percent))
    return percent


if __name__ == '__main__':
    import argparse, os
    from PIL import Image

    default_quality = 85
    supported_formats = {"jpg", "png"}

    parser = argparse.ArgumentParser(description="Image minifier")
    parser.add_argument("file", help="Minifies the target file")
    parser.add_argument("-q", "--quality", type=int, default=default_quality, help="Quality of image (default: " + str(default_quality) + "%)")
    args = parser.parse_args()
    print("<" + "=" * 20 + " [ Image Minifier ] " + "=" * 20 + ">")
    print("Image: ", args.file)
    newfile = args.file.split(".")
    min_file = ".".join(newfile[0:-1]) + ".min." + newfile[-1]
    print("Target: ", min_file)
    print("Quality: ", str(args.quality) + "%")

    if args.file.lower() == "run":
        import time

        print("<" + "=" * 60 + ">")
        while True:
            for filename in os.listdir():
                newfile = filename.split(".")
                min_file = ".".join(newfile[0:-1]) + ".min." + newfile[-1]
                if not newfile[-1].lower() in supported_formats:
                    continue
                if not os.path.exists(min_file) and filename.split(".")[-2] != "min":
                    print("Image: ", filename)
                    print("Image size: ", formatFileSize(os.path.getsize(filename)))
                    compressMe(filename, default_quality, True)
                    print("Target: ", min_file)
                    print("Minified size: ", formatFileSize(os.path.getsize(min_file)))
                    print("<" + "=" * 60 + ">")
            time.sleep(1)

    else:
        if not os.path.exists(args.file):
            print("File not found!")
            exit()
        if not (newfile[-1].lower() in supported_formats):
            print(newfile[-1].lower() + " is not supported format. Supported: " + ", ".join(supported_formats))
            exit()

        compressMe(args.file, default_quality, True)

        print("Image size: ", formatFileSize(os.path.getsize(args.file)))
        print("Minified size: ", formatFileSize(os.path.getsize(min_file)))
