import re

# Simple patterns for common sensitive data
SENSITIVE_PATTERNS = {
    "email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    "password": r'(?i)(password|passwd|pwd|pw)\s*[:=]\s*(\S+)',
    "api_key": r'(?i)(api[_-]?key|secret|token)\s*[:=]\s*(\S+)',
}

def mask_sensitive_info(text: str) -> str:
    """Masks potential sensitive information in user commands or logs."""
    masked_text = text
    
    # Masking Email
    masked_text = re.sub(SENSITIVE_PATTERNS["email"], "[EMAIL_MASKED]", masked_text)
    
    # Masking Password/Secret values (keeping the key, masking the value)
    def mask_value(match):
        key = match.group(1)
        return f"{key}: [MASKED]"
    
    masked_text = re.sub(SENSITIVE_PATTERNS["password"], mask_value, masked_text)
    masked_text = re.sub(SENSITIVE_PATTERNS["api_key"], mask_value, masked_text)
    
    return masked_text

if __name__ == "__main__":
    test_str = "My email is test@example.com and my password: 12345"
    print(f"Original: {test_str}")
    print(f"Masked: {mask_sensitive_info(test_str)}")
