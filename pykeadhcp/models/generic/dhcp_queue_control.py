from pykeadhcp.models.generic.config import CommonConfig


class DHCPQueueControl(CommonConfig):
    enable_queue: bool
    queue_type: str
    capacity: int
