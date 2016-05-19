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

Exampples
=========

    
    mne 'it will be shown every day until the end of the month.' -d  
    
    mne 'it will be shown on the first day of the following months.' -m  -d 1 
    
    mne 'it will be shown every day at 15:30' -m  -d  -r 15 -e 30 
    
    mne 'it will be show every month at the current day/time.' -m  
    
    





