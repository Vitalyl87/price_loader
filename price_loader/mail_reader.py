import csv
import email
from email.utils import parseaddr
from io import StringIO
from typing import AsyncGenerator

from aioimaplib import aioimaplib
from fastapi import HTTPException

from price_loader.logger import logger
from price_loader.schemas import DetailSchema


class MailReader:
    """Class for read data from mailbox"""

    def __init__(self, login: str, password: str, server: str):
        self.login: str = login
        self.password: str = password
        self.server: str = server
        self.client: aioimaplib.IMAP4_SSL = None

    async def create_inbox_connection(self) -> None:
        self.client = aioimaplib.IMAP4_SSL(self.server)
        await self.client.wait_hello_from_server()

        status, _ = await self.client.login(self.login, self.password)

        if status != "OK":
            logger.error("Authorization error via imap - check credentials in config.")
            raise HTTPException(
                401, "Authorization error via imap - check credentials in config."
            )

        status, _ = await self.client.select("INBOX")

        if status != "OK":
            logger.error("Error connecting to the inbox folder.")
            raise HTTPException(403, "Error connecting to the inbox folder.")

    async def close_connection(self) -> None:
        if self.client:
            await self.client.logout()

    async def search_letters(self, box: str) -> list[int] | None:
        if self.client:
            status, messages = await self.client.search(box)

            if status != "OK":
                logger.info(f"Couldn't search for emails based on the criterion {box}.")
            elif len(messages[0]) == 0:
                logger.info("All messages were read earlier.")
            else:
                return [int(msg) for msg in messages[0].split()]

    async def read_messages(
        self, messages: list[int], configs: dict[str : dict[str, str]]
    ) -> AsyncGenerator[list[dict[str, str]]]:
        if self.client and messages:
            for msg_id in messages:

                status, msg_data = await self.client.fetch(int(msg_id), "RFC822")

                if status == "OK":
                    raw_email = msg_data[1]
                    email_message = email.message_from_bytes(raw_email)

                    _, sender = parseaddr(email_message["From"])

                    if sender in configs.keys():
                        current_dict_config = configs[sender]
                        for part in email_message.walk():
                            if part.get_content_disposition() == "attachment":
                                filename = part.get_filename()
                                if filename and filename.endswith(".csv"):
                                    file_data = part.get_payload(decode=True)
                                    file_data = file_data.decode("utf-8-sig")

                                    async for chunk in self.read_csv_by_chunks(
                                        file_data, chunk_size=1000
                                    ):
                                        yield self.process_chunk(
                                            chunk, current_dict_config
                                        )

    async def __aenter__(self):
        try:
            await self.create_inbox_connection()
        except TimeoutError as ex:
            logger.error(
                f"Couldn't reach the mail server for a long time, check server in config. {ex}"
            )
            raise HTTPException(
                502,
                "Couldn't reach the mail server for a long time, check server in config.",
            )
        return self

    async def __aexit__(self, ex_type, val, ecx_tb):
        if ex_type:
            logger.error(f"Error occured: {ex_type}, {val}, {ecx_tb}")
        await self.close_connection()

    async def read_csv_by_chunks(
        self, csv_string: str, chunk_size: int
    ) -> AsyncGenerator[list[dict[str, str]], None]:
        reader = csv.DictReader(StringIO(csv_string), delimiter=";", quotechar='"')
        chunk = []
        for row in reader:
            chunk.append(row)

            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    def process_chunk(
        self, chunk: list[dict[str, str]], current_dict_config: dict[str, str]
    ):
        details = []
        for row in chunk:
            new_row = {
                current_dict_config[k]: row[k]
                for k in row.keys()
                if k in current_dict_config.keys()
            }
            try:
                new_det = DetailSchema(**new_row)
                details.append(new_det)
            except Exception as ex:
                logger.error(
                    f"There is a problem with the string during parsing of the csv file (there may be typos in the file itself). Mistake: {ex}"
                )
        return details
