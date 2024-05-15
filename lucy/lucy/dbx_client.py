import dropbox  # type: ignore[import-untyped]

from lucy.config import Config


# pylint: disable=too-few-public-methods
class DropboxClient:

    def __init__(self, link: str = Config.ATCODER_TESTCASES_DROPBOX_LINK):
        self.shared_link = dropbox.files.SharedLink(link)

        token = Config.DROPBOX_TOKEN
        self.dbx = dropbox.Dropbox(token)

    def download(self, path: str, dest: str) -> None:
        self.dbx.sharing_get_shared_link_file_to_file(dest, self.shared_link.url, path)
