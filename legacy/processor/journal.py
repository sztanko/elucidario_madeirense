# pylint: disable=missing-class-docstring
import json
import logging
import sys
import termios
import tty


def read_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
    except KeyboardInterrupt:
        return "Ctrl-C"
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key


class Journal:
    def __init__(self, filename):
        self.filename = filename
        self.journal = {}
        self.logger = logging.getLogger(__name__)
        self._load()

    def in_journal(self, i, term):
        if i in self.journal:
            if self.journal[i]["term"] != term:
                raise Exception(
                    f"Term {term} is not the same as {self.journal[i]['term']}. Looks like adjust journal is corrupted"
                )
            # Log instead of print
            self.logger.info(f"Article {self.journal[i]['term']} was already adjusted to {self.journal[i]['decision']}")
            return self.journal[i]["decision"] == "m"
        return None

    def log(self, i, term, decision):
        self.logger.info("Logging the decision")
        out = {"i": i, "term": term, "decision": decision}
        self.logger.info(out)
        self.journal[i] = out

    def save(self):
        self.logger.info("Saving journal...")
        with open(self.filename, "w") as f:
            f.write(json.dumps(self.journal, indent=2))
        self.logger.info(f"Saved {len(self.journal)} decisions")

    def _load(self):
        count = 0
        try:
            with open(self.filename, "r") as f:
                journal_str = json.loads(f.read())
                for k, v in journal_str.items():
                    self.journal[int(k)] = v
                    count += 1
            self.logger.info(f"Loaded {count} decisions")
        except FileNotFoundError:
            self.logger.warning(f"File {self.filename} not found, starting with empty journal.")

    def ask_if_merge(self, i, term):
        previous_decision = self.in_journal(i, term)
        if previous_decision is not None:
            return previous_decision
        print("Press 'm' to merge with previous article, 's' to split it as a standalone article, or 'c' to cancel")
        key = read_key()
        while key not in ["m", "s", "c"]:
            key = read_key()
        if key == "c":
            self.logger.info("Cancelling")
            self.save_journal()
            sys.exit(1)
        self.log_journal(i, term, key)
        return key == "m"
