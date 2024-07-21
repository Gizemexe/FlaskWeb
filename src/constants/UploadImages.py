import random
import os

def uploadimage(file):
    r = random.Random()
    path = "-1"
    random_num = r.randint(0, 1000000)
    if file is not None and file.content_length > 0:
        extension = os.path.splitext(file.filename)[1]
        if extension.lower() == ".jpg" or extension.lower() == ".jpeg" or extension.lower() == ".png":
            try:
                filename = str(random_num) + os.path.basename(file.filename)
                server_path = os.path.join(os.getcwd(), "Content/Images/")
                path = os.path.join(server_path, filename)
                file.save(path)
                path = "Content/Images/" + filename
            except Exception as ex:
                path = "-1"
                raise ex
        else:
            print("<script>alert('Only .JPG , .JPEG , .PNG Formats Are Allowed')</script>")
    else:
        print("<script>alert('Please Select a File')</script>")
        path = "-1"
    return path

