from RFM9X import RFM9X
#from nolocks import DataMonitor
from DataMonitor import DataMonitor
rfm9x = RFM9X(20)
while(True):
    record = DataMonitor(rfm9x)

    data = record.read_and_send_data() 
    record.unpack_data(data)



