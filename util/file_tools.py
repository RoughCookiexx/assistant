import base64

def base64_to_file(encoded_string, filename):
    try:
        decoded_string = base64.b64decode(encoded_string)

        with open(filename, "wb") as file:
            file.write(decoded_string)

        print("File successfully created: {}".format(filename))

    except Exception as e:
        print("Error: {}".format(e))

