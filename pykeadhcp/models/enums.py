from enum import Enum


class StatusEnum(str, Enum):
    ready = "ready"
    retrying = "retrying"
    failed = "failed"


class ReservationMode(str, Enum):
    disabled = "disabled"
    out_of_pool = ("out-of-pool",)
    r_global = "global"
    all = "all"


class DDNSReplaceClientNameEnum(str, Enum):
    when_present = "when-present"
    never = "never"
    always = "always"
    when_not_present = "when-not-present"


class Lease6TypeEnum(str, Enum):
    iana = "IA_NA"
    iapd = "IA_PD"
