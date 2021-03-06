"""
Module for Serialization and Deserialization of a KNX Tunnelling Request information.

Tunnelling requests are used to transmit a KNX telegram within an existing KNX tunnel connection.
"""
import logging

from xknx.exceptions import CouldNotParseKNXIP, UnsupportedCEMIMessage

from .body import KNXIPBody
from .cemi_frame import CEMIFrame, CEMIMessageCode
from .knxip_enum import KNXIPServiceType

logger = logging.getLogger("xknx.log")


class TunnellingRequest(KNXIPBody):
    """Representation of a KNX Tunnelling Request."""

    # pylint: disable=too-many-instance-attributes

    service_type = KNXIPServiceType.TUNNELLING_REQUEST

    HEADER_LENGTH = 4

    def __init__(
        self,
        xknx,
        communication_channel_id: int = 1,
        sequence_counter: int = 0,
        cemi: CEMIFrame = None,
    ):
        """Initialize TunnellingRequest object."""
        super().__init__(xknx)

        self.communication_channel_id = communication_channel_id
        self.sequence_counter = sequence_counter
        self.cemi = (
            cemi
            if cemi is not None
            else CEMIFrame(xknx, code=CEMIMessageCode.L_Data_REQ)
        )

    def calculated_length(self):
        """Get length of KNX/IP body."""
        return TunnellingRequest.HEADER_LENGTH + self.cemi.calculated_length()

    def from_knx(self, raw):
        """Parse/deserialize from KNX/IP raw data."""

        def header_from_knx(header):
            """Parse header bytes."""
            if header[0] != TunnellingRequest.HEADER_LENGTH:
                raise CouldNotParseKNXIP("connection header wrong length")
            if len(header) < TunnellingRequest.HEADER_LENGTH:
                raise CouldNotParseKNXIP("connection header wrong length")
            self.communication_channel_id = header[1]
            self.sequence_counter = header[2]
            return TunnellingRequest.HEADER_LENGTH

        pos = header_from_knx(raw)
        try:
            pos += self.cemi.from_knx(raw[pos:])
        except UnsupportedCEMIMessage as unsupported_cemi_err:
            logger.debug("CEMI not supported: %s", unsupported_cemi_err)
            # Set cemi to None - this is checked in Tunnel() to send Ack even for unsupported CEMI messages.
            self.cemi = None
            return len(raw)
        return pos

    def to_knx(self):
        """Serialize to KNX/IP raw data."""

        def header_to_knx():
            """Serialize header."""
            cri = []
            cri.append(TunnellingRequest.HEADER_LENGTH)
            cri.append(self.communication_channel_id)
            cri.append(self.sequence_counter)
            cri.append(0x00)  # Reserved
            return cri

        data = []
        data.extend(header_to_knx())
        data.extend(self.cemi.to_knx())
        return data

    def __str__(self):
        """Return object as readable string."""
        return (
            '<TunnellingRequest communication_channel_id="{}" '
            'sequence_counter="{}" cemi="{}" />'.format(
                self.communication_channel_id, self.sequence_counter, self.cemi
            )
        )
