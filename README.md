# ReactionTime-PyQt5
Support interface for measuring choice reaction time. Well documented.

This project was created with the intent of providing a medium for syncronizing an automatic visual
command with another source that would provide information about user response. In this case the visual
command consists of the lights on the screen and the user response is captured by an electromyography
(EMG) device.

The syncronization is possible because both this interface and the data acquisition software for the 
EMG provide the time stamp for when they started running, using the computer clock.

The user can select which lights to use, the number of elements in the sequence (how many lights will
appear in total), the period that each light will stay on for, and at what instant each light will turn on.
The instant is relative to the test blocks, that are the time divisions present in the test protocol.
All blocks are the same lenght, and there will be only one light associated with each block

In its current state, the interface is limited to only allow blocks of 15 seconds, and the lights can
only be lit on the 5th, 6th, 7th, 8th, 9th, and 10th second of their respective block.
The sequence in which the lights will be lit can be randomly shuffled, as well as the instant that they
will be switched on.

The interface is optimized to be used with at least two displays, so that both windows (the one with the
lights and the one with the controls) can fully operate without negatively interfering with eachother.

Finally, the logs for the session can be saved in a text file, formated in such a way that the relevant
information can be easily extracted with, for instance, MATLAB, where the user can synchronize it with
another source to be able to systematically measure the choice reaction time.
