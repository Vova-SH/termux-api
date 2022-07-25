"""MOVE TO FOLDER"""


class WiFiInfo:
    def __init__(
        self,
        bssid,
        frequency,
        ip,
        link_speed_mbps,
        mac_address,
        network_id,
        rssi,
        ssid,
        ssid_hidden,
        supplicant_state,
    ):
        self.update(
            bssid,
            frequency,
            ip,
            link_speed_mbps,
            mac_address,
            network_id,
            rssi,
            ssid,
            ssid_hidden,
            supplicant_state,
        )

    @classmethod
    def empty(cls):
        return cls(
            "00:00:00:00:00:00",
            0,
            "0.0.0.0",
            0,
            "00:00:00:00:00:00",
            0,
            0,
            "",
            False,
        )

    def update(
        self,
        bssid,
        frequency,
        ip,
        link_speed_mbps,
        mac_address,
        network_id,
        rssi,
        ssid,
        ssid_hidden,
        supplicant_state,
    ):
        self.bssid = bssid  # XX:XX:XX:XX:XX:XX
        self.frequency = frequency  # MHz
        self.ip = ip  # XXX.XXX.XXX.XXX
        self.link_speed_mbps = link_speed_mbps
        self.mac_address = mac_address  # XX:XX:XX:XX:XX:XX
        self.network_id = network_id
        self.rssi = rssi
        self.ssid = ssid
        self.ssid_hidden = ssid_hidden
        self.supplicant_state = supplicant_state  # ASSOCIATED ASSOCIATING AUTHENTICATING COMPLETED DISCONNECTED DORMANT FOUR_WAY_HANDSHAKE GROUP_HANDSHAKE INACTIVE INTERFACE_DISABLED INVALID SCANNING UNINITIALIZED
