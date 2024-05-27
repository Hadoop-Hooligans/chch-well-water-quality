import base64


def encode_well(well_code):

    # Define the encode function (replace this with your actual encoding logic)
    def encode_string(string):
        return base64.b64encode(string.encode()).decode()

    # Create the encoded well number
    encoded_well_number = encode_string(well_code)

    # Construct the href URL
    base_url = "https://www.ecan.govt.nz/data/well-search/welldetails/"
    href = f"{base_url}{encoded_well_number}/{encoded_well_number}"

    return href
