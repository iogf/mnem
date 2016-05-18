mne
===

A note reminder that uses dzen2 to display notes.

Exampples
=========

    
    mne -m * -d * 'it will be shown every day.'
    
    mne -m * -d 1 'it will be shown every months at its first days'
    
    mne -m * -d * -r 15 -e 30 'it will be shown every days at 15:30'
    
    mne -m * 'it will be show every month at a random day and time.'
    
    mne -m * -d * -h 12 'it will be shown always at midday'
    
    mne -m * -h 15 -i 30 'it will be shown once per month at 15:30.'
    
    mne -y 2019 -m 1 -d 1 -h 15 -i 30 'It will be shown on 1/1/2019 at 15:30h.'
    

