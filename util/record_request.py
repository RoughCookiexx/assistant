from flask import request
import shlex

def flask_request_to_curl(req, filepath):
    """
    Convert a Flask request to a cURL command and write it to a file.

    Parameters:
    - req: Flask request object
    - filepath: path to the file where the cURL command should be written
    """
    # Start building the curl command
    command = ['curl']

    # Add method if not GET
    method = req.method
    if method != 'GET':
        command.append('-X')
        command.append(shlex.quote(method))

    # Add headers
    for header, value in req.headers:
        # Skip the Host header since curl sets it automatically
        if header.lower() == 'host':
            continue
        # Format header: -H 'Header: value'
        header_str = f"{header}: {value}"
        command.append('-H')
        command.append(shlex.quote(header_str))

    # Determine the data payload, if any
    data = None
    content_type = req.headers.get('Content-Type', '')

    # Try to find data in form, json or data
    if req.data:
        # Prefer raw data if present
        data = req.data
    elif req.form:
        # We need to encode form data
        # Convert ImmutableMultiDict to dictionary
        # Use urllib.parse.urlencode
        from urllib.parse import urlencode
        form_data = req.form.to_dict(flat=False)
        # urlencode with doseq=True for multiple values per key
        data = urlencode(form_data, doseq=True).encode('utf-8')
    elif req.json:
        import json
        data = json.dumps(req.json).encode('utf-8')

    if data:
        # Add data to command with --data-binary to preserve binary and newlines
        # Convert bytes to string. If bytes, decode with utf-8, else str()
        if isinstance(data, bytes):
            data_str = data.decode('utf-8')
        else:
            data_str = str(data)
        command.append('--data-binary')
        command.append(shlex.quote(data_str))

    # Build URL including query string
    url = req.url

    command.append(shlex.quote(url))

    # Join the command and write to file
    curl_command = ' '.join(command) + '\n'

    with open(filepath, 'w') as f:
        f.write(curl_command)

    return curl_command  # Optionally return it as well

