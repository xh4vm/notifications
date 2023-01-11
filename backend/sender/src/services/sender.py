import nest_asyncio
nest_asyncio.apply()
import asyncio
from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path
from email import encoders
import mimetypes
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import SMTP
from loguru import logger


class BaseSender(ABC):

    @abstractmethod
    async def send(self, **kwargs) -> None:
        '''Метод отправки сообщения'''


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

    def attached_file(self, file_path: str) -> MIMEBase:
        ctype, encoding = mimetypes.guess_type(file_path)

        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        
        maintype, subtype = ctype.split('/', 1)
        
        file = MIMEBase(maintype, subtype)

        with open(file_path, 'rb') as fd:
            content = fd.read()
            file.set_payload(content)
        
        encoders.encode_base64(file)
        file.add_header('Content-Disposition', 'attachment', filename=file_path)

        return file

    async def send(self, to: str, subject: str, data: str, file_path: Optional[str] = None, **kwargs):
        message = MIMEMultipart()

        message['From'] = self.mail_from
        message['To'] = to
        message['Subject'] = subject

        body = MIMEText(data)
        message.attach(body)

        if file_path is not None and Path(file_path).is_file():
            attached_file = self.attached_file(file_path)
            message.attach(attached_file)
        
        await self.conn.sendmail(self.mail_from, to, message.as_string())
