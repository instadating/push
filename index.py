from cryptography.hazmat.primitives.asymmetric import ec
import base64

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

def generate_vapid_keys():
    # Generate EC private key (P-256 curve)
    private_key = ec.generate_private_key(ec.SECP256R1())

    # Extract raw private key (32 bytes)
    private_numbers = private_key.private_numbers()
    private_key_bytes = private_numbers.private_value.to_bytes(32, "big")

    # Extract raw public key (uncompressed)
    public_numbers = private_key.public_key().public_numbers()
    x = public_numbers.x.to_bytes(32, "big")
    y = public_numbers.y.to_bytes(32, "big")
    public_key_bytes = b"\x04" + x + y

    return {
        "publicKey": b64url(public_key_bytes),
        "privateKey": b64url(private_key_bytes)
    }

if __name__ == "__main__":
    keys = generate_vapid_keys()
    print("\n VAPID KEYS GENERATED\n")
    print("PUBLIC_VAPID_KEY =", keys["publicKey"])
    print("PRIVATE_VAPID_KEY =", keys["privateKey"])
