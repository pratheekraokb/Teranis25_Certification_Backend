# Certificate Verification API

This API is designed to verify certificates using a unique code. It loads data from a JSON file and searches for the corresponding certificate image in a specified Google Drive folder.

## Features
- Verify a certificate by providing a unique 10-character code.
- Fetch user details from `data.json`.
- Retrieve certificate image details from Google Drive.

## API Endpoint

### Verify Certificate
**Endpoint:** `GET /verifycertificate/<string:code>/`

**Parameters:**
- `code` (string, required): A 10-character unique certificate code.

**Response:**
- If the code is valid:
  ```json
  {
    "message": "valid code",
    "user_details": {
        "department": "CSE",
        "email": "xyz@gmail.com",
        "event_date": "27/02/2025",
        "event_name": "Debugging In Python",
        "name": "xyz",
        "phone": 9102518415,
        "semester": "S2 CS A"
    },
    "certificate_details": {
        "download_link": "DOWNLOADABLE LINK",
        "filename": "DIP2DJQ9M1.png",
        "view_link": "VIEW LINK"
    },
  }
  ```
- If the code is invalid:
 ```json
{
    "message": "invalid code"
}
```


