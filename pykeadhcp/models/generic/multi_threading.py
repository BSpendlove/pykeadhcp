from pykeadhcp.models.generic.config import CommonConfig


class MultiThreading(CommonConfig):
    enable_multi_threading: bool
    thread_pool_size: int
    packet_queue_size: int
