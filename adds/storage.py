import os
from urllib.request import urlopen

from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from vercel.blob import BlobClient


class VercelBlobStorage(Storage):
    """Store uploaded media in a public Vercel Blob store."""

    def _token(self):
        token = os.environ.get("BLOB_READ_WRITE_TOKEN")
        if not token:
            raise ImproperlyConfigured(
                "Connect a Vercel Blob store and set BLOB_READ_WRITE_TOKEN."
            )
        return token

    def _save(self, name, content):
        content.open("rb")
        try:
            body = content.read()
        finally:
            content.close()

        with BlobClient(token=self._token()) as client:
            blob = client.put(
                name,
                body,
                access="public",
                add_random_suffix=True,
                content_type=getattr(content, "content_type", None),
            )
        return blob.url

    def _open(self, name, mode="rb"):
        with urlopen(name) as response:
            return ContentFile(response.read(), name=name.rsplit("/", 1)[-1])

    def exists(self, name):
        # Blob names receive a random suffix during upload, so collisions are avoided.
        return False

    def url(self, name):
        if name.startswith(("https://", "http://")):
            return name
        return super().url(name)

    def delete(self, name):
        if name.startswith(("https://", "http://")):
            with BlobClient(token=self._token()) as client:
                client.delete(name)
