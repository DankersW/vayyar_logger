# Demo script

Location: Vinnter office - room F
Mounting: Ceiling mounted with Xmin=0.7 Xmax=2.7 Ymin=1.8 Ymax=1.8 height=2.4
Presentation: https://vinngroup-my.sharepoint.com/:p:/g/personal/woda_vinngroup_net/EeOguRyv4MpAgBYzEd2EHoABnkbXS0RJlrPz6ZyXWxpS4g?e=8Z08QH

## Scenarios

The demo will be appoximently 10-15 minutes, where the setup will be shown, as well as the events that we receive from
the sensor.

**1) One person in the room:**
Start of with a closed and empty room. The monitoring tool should indicate that the room is free. One person will walk into 
the room, walking around for one minute, then leaving the room, closing the door. 
The expected outcome will be that the monitoring tool shows that the room has been occupieds for 1 minute. Use the timestamps
to varify the events.

**2) Two persons in the room:**
Same setup as 1) but with two people.
The expected outcome will be that room became occupied (on the monitor) from when the first person entered the room, and became
free from when the last person left the room.

**3) Walking in and out the room fast 3 times:**
Walking in and out the room like one is picking up (or dropping off) something 3 times. 
Expected outcome will be that 3 occupied spikes are seen in the monitoring tool. Depending on how fast the person went in 
and out some events might not be picked up. 

**4) Triggering a fall event**
Walk into the room and lay on the floor for 1 minute. This will (in an ideal case) trigger a fall event. 
Expected outcome is that the fall event is pick up. _Note that this event is hard to trigger_ 

**5) Room edges**
Walk around the outside of the room, mimicking people walking past. 
Expected outcome is to not trigger the room becoming occupied. _Note that and exidental room occupied event could be triggered_
