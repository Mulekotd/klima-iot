from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import blake2b
from threading import Lock
from time import sleep, time_ns


KLIMA_EPOCH = datetime(2026, 1, 1, tzinfo=timezone.utc)
TIMESTAMP_BITS = 41
DEVICE_BITS = 10
SEQUENCE_BITS = 12

MAX_DEVICE_KEY = (1 << DEVICE_BITS) - 1
MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1
MAX_TIMESTAMP = (1 << TIMESTAMP_BITS) - 1


@dataclass(frozen=True)
class SnowflakeParts:
    generated_at: datetime
    device_key: int
    sequence: int


class SnowflakeIdGenerator:
    """64-bit IDs: timestamp_ms | device_key | sequence."""

    def __init__(self, epoch: datetime = KLIMA_EPOCH) -> None:
        self._epoch_ms = self._to_unix_millis(epoch)
        self._last_timestamp_ms = -1
        self._sequence = 0
        self._lock = Lock()

    def generate(self, device_id: str, generated_at: datetime | None = None) -> str:
        with self._lock:
            timestamp_ms = self._to_unix_millis(generated_at)
            if timestamp_ms < self._last_timestamp_ms:
                timestamp_ms = self._last_timestamp_ms

            if timestamp_ms == self._last_timestamp_ms:
                self._sequence = (self._sequence + 1) & MAX_SEQUENCE
                if self._sequence == 0:
                    timestamp_ms = self._wait_next_millis(self._last_timestamp_ms)
            else:
                self._sequence = 0

            self._last_timestamp_ms = timestamp_ms
            elapsed_ms = timestamp_ms - self._epoch_ms
            if elapsed_ms < 0:
                raise ValueError("Snowflake timestamp cannot be before Klima epoch.")
            if elapsed_ms > MAX_TIMESTAMP:
                raise ValueError("Snowflake timestamp exceeded the 41-bit limit.")

            device_key = self.device_key(device_id)
            snowflake_id = (
                (elapsed_ms << (DEVICE_BITS + SEQUENCE_BITS))
                | (device_key << SEQUENCE_BITS)
                | self._sequence
            )
            return str(snowflake_id)

    def parse(self, snowflake_id: str | int) -> SnowflakeParts:
        raw_id = int(snowflake_id)
        sequence = raw_id & MAX_SEQUENCE
        device_key = (raw_id >> SEQUENCE_BITS) & MAX_DEVICE_KEY
        elapsed_ms = raw_id >> (DEVICE_BITS + SEQUENCE_BITS)
        generated_at = datetime.fromtimestamp(
            (self._epoch_ms + elapsed_ms) / 1000,
            tz=timezone.utc
        )
        return SnowflakeParts(
            generated_at=generated_at,
            device_key=device_key,
            sequence=sequence
        )

    def device_key(self, device_id: str) -> int:
        digest = blake2b(device_id.encode("utf-8"), digest_size=2).digest()
        return int.from_bytes(digest, byteorder="big") & MAX_DEVICE_KEY

    def _wait_next_millis(self, current_timestamp_ms: int) -> int:
        next_timestamp_ms = self._to_unix_millis(None)
        while next_timestamp_ms <= current_timestamp_ms:
            sleep(0.001)
            next_timestamp_ms = self._to_unix_millis(None)
        return next_timestamp_ms

    def _to_unix_millis(self, value: datetime | None) -> int:
        if value is None:
            return time_ns() // 1_000_000
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return int(value.timestamp() * 1000)


snowflake_ids = SnowflakeIdGenerator()
