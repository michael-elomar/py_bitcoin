from .utils import hash256
from .types import StreamTypes
from .script import Script


class TxIn:
    def __init__(self, prev_tx: "Tx", prev_index, script_sig: Script = None, sequence=0xffffffff) -> "TxIn":
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig

        self.sequence = sequence

    def __repr__(self) -> str:
        return f"{self.prev_tx.hex()}:{self.prev_index}"


class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime, testnet=False) -> "Tx":
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet

    def __repr__(self) -> str:
        tx_ins = ""
        for tx_in in self.tx_ins:
            tx_ins += repr(tx_in) + "\n"

        tx_outs = ""
        for tx_out in self.tx_outs:
            tx_outs += repr(tx_out) + "\n"

        return f"tx: {self.id()}\nversion: {self.version}\ntx_ins:{tx_ins}\ntx_outs: {tx_outs}\n locktime: {self.locktime}."

    def id(self):
        """Human read hexadecimal of the transaction hash"""
        return self.hash().hex()

    def hash(self):
        """Binary hash of the legacy serialization"""
        return hash256(self.serialize())[::-1]

    @classmethod
    def parse(cls, stream: StreamTypes) -> "Tx":
        version = int.from_bytes(stream.read(4), "little")
