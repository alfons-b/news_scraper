class BaseDiscovery:
    """
    untuk mekanisme discovery URL.
    """

    def discover(self, source):
        raise NotImplementedError(
            "Subclass harus mengimplementasikan methon discover()."
        )
    