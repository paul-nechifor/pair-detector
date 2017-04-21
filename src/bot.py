from . import config, reddit, utils


class Bot(object):

    def __init__(self):
        self.config = config.Config()
        self.reddit_handler = reddit.RedditHandler(self.config)

    def start(self):
        utils.make_dirs(
            self.config.found_dir,
            self.config.found_crop_dir,
            self.config.tmp_dir,
        )
        for s in self.reddit_handler.stream_submissions():
            self.handle_submission(s)

    def handle_submission(self, submission):
        print 'new submission'
        with submission:
            if submission.image.dets:
                print 'saving', submission.uuid
                submission.copy_to_found()


if __name__ == '__main__':
    Bot().start()
