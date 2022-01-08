from pypresence import Presence
import time

client_id = '927551550275067924'
RPC = Presence(client_id,pipe=0)  # Initialize the client class
RPC.connect() # Start the handshake loop
startTime = time.time()
RPC.update(details="In Main Menu", state="Waiting. . .", large_image="icon", large_text="Text RPG 0.0.1", start=startTime) # First update

def update(dat1, dat2):
    detaildat = dat1
    statedat = dat2

def gettime():
    return startTime

def getrpc():
    return RPC
