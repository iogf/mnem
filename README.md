mne
===

A note reminder that uses dzen2 to display notes

Install
=======

    pip2 install libdae
    pip2 install mne

Note: It demands dzen2 menu to display the reminders.
It is problable that your linux distribution lets you easily
install that.

**See:** https://github.com/robm/dzen

Screenshot
==========

![screenshot-1](screenshot-1.jpg)

Usage
=====

mne accepts the following parameters:

    mne -h

When mne doesnt find one of the parameters -i -m, -y, -u, -d it assumes the current values 
for years, minutes, days etc. When it finds these parameters and they aren't followed by
values then it assumes all possible values for the given parameter.

So, if you run the following command:

    mne 'this is a note' -u -i 40

It will assume years=current, months=current, days=current, hours=24, minutes=40

**Display a note daily**

    mne 'it will be shown every day until the end of the month.' -d  

**Display a note monthly**
  
    mne 'Title
    It is a message.
    ' -m 

**Display a note monthly on a specific day**
  
    mne 'it will be shown on the first day of the following months.' -m  -d 1 
  

**Display a note daily at a specific time**
  
    mne 'it will be shown every day at 15:30' -m  -d  -r 15 -e 30 
    
    
    






