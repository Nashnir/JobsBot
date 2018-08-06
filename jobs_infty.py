import subprocess
import time


def main_infty():
    while True:
        # run until the program encounters too many errors
        subprocess.run(["python", "jobs_cli.py", "-v 1", "-u 1"])
        # sleep for an hour
        time.sleep(60*60)


if __name__ == "__main__":
    main_infty()