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


class LoggerLevelEnum(str, Enum):
    critical = "CRITICAL"
    error = "ERROR"
    warning = "WARNING"
    info = "INFO"
    debug = "DEBUG"


class DHCPSocketTypeEnum(str, Enum):
    raw = "raw"
    udp = "udp"


class OutboundInterfaceEnum(str, Enum):
    same_as_inbound = "same-as-inbound"
    use_routing = "use-routing"


class DatabaseTypeEnum(str, Enum):
    memfile = "memfile"
    mysql = "mysql"
    postgresql = "postgresql"


class DatabaseOnFailEnum(str, Enum):
    stop_retry_exit = "stop-retry-exit"
    serve_retry_exit = "serve-retry-exit"
    serve_retry_continue = "serve-retry-continue"


class HostReservationIdentifierEnum(str, Enum):
    duid = "duid"
    hw_address = "hw-address"
    circuit_id = "circuit-id"
    client_id = "client-id"
    flex_id = "flex-id"


class NCRProtocolEnum(str, Enum):
    udp = "UDP"
    tcp = "TCP"


class NCRFormatEnum(str, Enum):
    json = "JSON"


class ServerIdTypeEnum(str, Enum):
    llt = "LLT"
    en = "EN"
    ll = "LL"


class AuthenticationTypeEnum(str, Enum):
    basic = "basic"


class RemoteMapTypeEnum(str, Enum):
    mysql = "mysql"
    postgresql = "postgresql"


class HAModeTypeEnum(str, Enum):
    load_balancing = "load-balancing"
    hot_standby = "hot-standby"


class HARoleTypeEnum(str, Enum):
    primary = "primary"
    secondary = "secondary"
    standby = "standby"


class HAStateTypeEnum(str, Enum):
    backup = "backup"
    communication_recovery = "communication-recovery"
    hot_standby = "hot-standby"
    load_balancing = "load-balancing"
    in_maintenance = "in-maintenance"
    partner_down = "partner-down"
    partner_in_maintenance = "partner-in-maintenance"
    passive_backup = "passive-backup"
    ready = "ready"
    synbcing = "syncing"
    terminated = "terminated"
    waiting = "waiting"
    unavailable = "unavailable"
    null = ""
