import argparse
from jobs.StackJobs import JobsBot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity (log more info)",
                        type=int, choices=[0, 1],
                        default=0)
    parser.add_argument("-u", "--update",
                        help="defines if the job targets should be updated - default: True",
                        type=int, choices=[0, 1],
                        default=1)
    args = parser.parse_args()
    try:
        # init the bot
        sj_bot = JobsBot(args.verbose)
        # update if necessary
        sj_bot.get_targets(should_update=args.update)
        # apply automatically
        sj_bot.apply_auto()
    except KeyboardInterrupt:
        print("program execution interrupted.\nExiting.")


if __name__ == "__main__":
    main()
