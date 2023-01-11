import nest_asyncio
nest_asyncio.apply()
import asyncio
from abc import ABC, abstractmethod
from typing import Optional
from email.message import EmailMessage
import mimetypes
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import send, SMTP
from loguru import logger


class BaseSender(ABC):

    @abstractmethod
    async def send(self, **kwargs) -> None:
        '''Метод '''


class SmtpSender(BaseSender):

    def __init__(self,
        hostname: str,
        username: str,
        domain: str,
        password: str,
        port: int = 25,
        conn: Optional[SMTP] = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._conn = conn
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.mail_from = f'{username}@{domain}'

    async def reconnect(self) -> SMTP:
        if self._conn is not None:
            self._conn.close()

        conn = SMTP(hostname=self.hostname, port=self.port, username=self.username, password=self.password)
        
        await conn.connect(self.hostname, port=self.port, username=self.username, password=self.password, start_tls=False)

        return conn

    @property
    def conn(self) -> SMTP:
        if self._conn is not None and self._conn.is_connected:
            return self._conn

        return asyncio.run(self.reconnect())

    async def send(self, to: str, subject: str, data: str, **kwargs):
        message = EmailMessage()

        message['From'] = self.mail_from
        message['To'] = to
        message['Subject'] = subject

        message.set_content(data)
        
        await self.conn.sendmail(self.mail_from, to, message.as_string())
