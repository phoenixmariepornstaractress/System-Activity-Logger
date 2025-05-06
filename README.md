# System Activity Logger

**System Activity Logger** is a Python-based monitoring utility for administrative and security auditing. It logs keyboard input, collects system data, executes command inputs, and securely stores and transmits information.

> **Important**: This software is for ethical, educational, and authorized use only. Unauthorized use is strictly prohibited.

## Features

* Real-time keyboard activity logging
* System, process, disk, and network information collection
* Custom command execution support
* Log file encryption and integrity hash generation
* Scheduled POST requests to a specified server
* Log archiving and secure email transmission
* Secure cleanup of logs and sensitive data

## Requirements

* Python 3.7 or newer
* `pynput`, `psutil`, `cryptography`, and other standard libraries

Install dependencies using:

```bash
pip install -r requirements.txt
```

## Usage

1. Configure script parameters:

   * Set `ip_address`, `port_number` for remote POST logging
   * Set `email_address`, `email_password`, `receiver_email` for email delivery

2. Run the script:

```bash
python system_activity_logger.py
```

## Contributing

We welcome contributions from the community! You can help improve features, fix bugs, enhance documentation, or refactor code.

### How to contribute

1. Fork the repository
2. Create a new branch:

   ```bash
   git checkout -b feature-name
   ```
3. Make your changes
4. Commit and push:

   ```bash
   git commit -m "Describe your change"
   git push origin feature-name
   ```
5. Open a pull request and describe what you've done

## License

This project is released for legitimate use only. Unauthorized, malicious, or unethical use is not allowed and may be illegal.

---

**Contact**: If you have suggestions or need assistance, feel free to open an issue or submit a pull request.
