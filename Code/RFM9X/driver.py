from RFM95X import RFM95X

rfm95x = RFM95X()

rfm95x.send(bytes("abcdefghijkl", "utf-8"))
