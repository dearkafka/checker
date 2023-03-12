#!/usr/bin/env python

import os
import sys
import argparse
import shutil
import configparser


def create_systemd_service(service_name, config_path):
    # Read config file
    config = configparser.ConfigParser()
    config.read(config_path)

    # Check if the service already exists
    service_file = f"/etc/systemd/system/{service_name}"
    if os.path.exists(service_file):
        print(f"{service_name} service already exists!")
        return

    # Create a new service file
    user = config.get("Service", "user")
    output_file = config.get("Service", "output_file")
    restart_sec = config.get("Service", "restart_sec")
    restart_policy = config.get("Service", "restart_policy")
    with open(service_file, "w") as f:
        f.write(
            f"[Unit]\n"
            f"Description={service_name}\n"
            f"After=network.target\n\n"
            f"[Service]\n"
            f"Type=simple\n"
            f"User={user}\n"
            f"ExecStart=checker {config_path}\n"
            f"StandardOutput=append:{output_file}\n"
            f"StandardError=append:{output_file}\n"
            f"Restart={restart_policy}\n"
            f"RestartSec={restart_sec}\n\n"
            f"[Install]\n"
            f"WantedBy=multi-user.target\n"
        )

    # Reload systemd and start the service
    os.system("systemctl daemon-reload")
    os.system(f"systemctl start {service_name}")
    print(f"Created {service_name} service!")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--create",
        action="store_true",
        help="create a new systemd service",
    )
    parser.add_argument("config_file", help="path to config file")
    args = parser.parse_args()

    # Check if the --create option was used
    if args.create:
        service_name = os.path.splitext(os.path.basename(args.config_file))[0]
        create_systemd_service(service_name, args.config_file)
        sys.exit()

    # Run the checker as usual
    from checker import main as checker_main

    checker_main(args.config_file)


if __name__ == "__main__":
    main()
