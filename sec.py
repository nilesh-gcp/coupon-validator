import json
import toml
import re

def validate_private_key(key: str) -> bool:
    """
    Validates that the private key:
    - Starts and ends with the correct PEM markers
    - Contains only valid base64 characters between the markers
    - Has at least one line of actual key data
    """
    if not key.startswith("-----BEGIN PRIVATE KEY-----") or not key.endswith("-----END PRIVATE KEY-----\n"):
        return False

    # Extract the content between the markers
    pattern = r"-----BEGIN PRIVATE KEY-----\n(.+?)\n-----END PRIVATE KEY-----\n"
    match = re.search(pattern, key, re.DOTALL)
    if not match:
        return False

    key_body = match.group(1).strip()
    # Basic base64 validation (not exhaustive)
    base64_chars = re.compile(r"^[A-Za-z0-9+/=\n\r]+$")
    return bool(base64_chars.match(key_body)) and len(key_body) > 100  # Arbitrary length check

def convert_json_to_toml(json_path, toml_path, section_name="gcp_service_account"):
    with open(json_path, "r") as f:
        creds = json.load(f)

    private_key = creds.get("private_key", "")
    if not validate_private_key(private_key):
        raise ValueError("❌ Invalid private key format. Please check your credentials.json.")

    toml_data = {
        section_name: {
            "type": creds.get("type"),
            "project_id": creds.get("project_id"),
            "private_key_id": creds.get("private_key_id"),
            "private_key": private_key,
            "client_email": creds.get("client_email"),
            "client_id": creds.get("client_id"),
            "auth_uri": creds.get("auth_uri"),
            "token_uri": creds.get("token_uri"),
            "auth_provider_x509_cert_url": creds.get("auth_provider_x509_cert_url"),
            "client_x509_cert_url": creds.get("client_x509_cert_url"),
        }
    }

    with open(toml_path, "w") as f:
        toml.dump(toml_data, f)

    print(f"✅ TOML file created at: {toml_path}")




def reformat_private_key(toml_path):
    data = toml.load(toml_path)
    key = data["gcp_service_account"]["private_key"]

    # If it's single-line, reformat it
    if "\\n" in key:
        key = key.replace("\\n", "\n")
    elif "-----BEGIN PRIVATE KEY-----" in key and "-----END PRIVATE KEY-----" in key:
        # Try splitting manually if no \n
        key = key.replace("-----BEGIN PRIVATE KEY-----", "-----BEGIN PRIVATE KEY-----\n")
        key = key.replace("-----END PRIVATE KEY-----", "\n-----END PRIVATE KEY-----\n")

    # Update TOML with triple-quoted multiline key
    data["gcp_service_account"]["private_key"] = key
    with open(toml_path, "w") as f:
        toml.dump(data, f)

    print("✅ Private key reformatted to multiline.")

# Example usage
reformat_private_key(".streamlit/secrets.toml")

# # Example usage
# convert_json_to_toml(
#     json_path="config/tnsdashboard-service-acct.json",
#     toml_path=".streamlit/secrets.toml"
# )