#!/usr/bin/python3


class MsgFrame(object):
    def __init__(self, msg_type: str, **kargs ) -> None:
        self.msg_type = msg_type
        self.param = kargs