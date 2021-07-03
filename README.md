mnem
====

A note reminder that uses dzen2 to display notes

Install
=======

    pip install python-daemon
    pip install mnem

Note: It demands dzen2 menu to display the reminders.
It is problable that your linux distribution lets you easily
install that.

**See:** https://github.com/robm/dzen

Screenshot
==========

![screenshot-1](screenshot-1.jpg)

Usage
=====

It is needed first to start mnem daemon, in order to do that just issue the command below:

    mnem-daemon

That is enough to have mnem daemon running. 
Figure out how to execute mnem-daemon at your graphical environment startup.

mnem accepts the following parameters:

~~~
usage: mnem [-h] [-i [MINUTES ...]] [-ii [FIND_MINUTES ...]] [-m [MONTHS ...]] 
            [-mm [FIND_MONTHS ...]] [-y [YEARS ...]] [-yy [FIND_YEARS ...]] [-u [HOURS ...]]
            [-uu [FIND_HOURS ...]] [-d [DAYS ...]] [-dd [FIND_DAYS ...]] [-a] [-f] [-r]
            [msg]

positional arguments:
  msg                   Messages

optional arguments:
  -h, --help            show this help message and exit
  -i [MINUTES ...], --minutes [MINUTES ...]
                        List of minutes.
  -ii [FIND_MINUTES ...], --find-minutes [FIND_MINUTES ...]
                        Find notes based on minute.
  -m [MONTHS ...], --months [MONTHS ...]
                        List of months.
  -mm [FIND_MONTHS ...], --find-months [FIND_MONTHS ...]
                        Find notes based on month.
  -y [YEARS ...], --years [YEARS ...]
                        List of years.
  -yy [FIND_YEARS ...], --find-years [FIND_YEARS ...]
                        Find notes based on year.
  -u [HOURS ...], --hours [HOURS ...]
                        List of hours.
  -uu [FIND_HOURS ...], --find-hours [FIND_HOURS ...]
                        Find notes based on hours.
  -d [DAYS ...], --days [DAYS ...]
                        List of days.
  -dd [FIND_DAYS ...], --find-days [FIND_DAYS ...]
                        Find notes based on days.
  -a, --add             Add a note.
  -f, --find            Find a note based on a regex.
  -r, --remove          Remove a note based on a regex.
[tau@fedora ~]$ 
    
~~~

When mnem doesnt find one of the parameters -i -m, -y, -u, -d it assumes the current values 
for years, minutes, days etc. When it finds these parameters and they aren't followed by
values then it assumes all possible values for the given parameter.

So, if you run the following command:

    mnem -a 'This is a note' -u -i 40

It will assume years=current, months=current, days=current, hours=[1, 2, 3, ...24], minutes=40.
That means it will display 'This is a note' the amount (24 - current-hour) in the current day.

**Display a note daily**

    mnem -a 'it will be shown every day until the end of the month.' -d  

**Display a note monthly**
  
    mnem -a 'Title It is a message.' -m 

The above command will assume days=current, years=current, minutes=current.
So, the message above will be displayed every month in the same time of the day
that the command was issued.

**Display a note monthly on a specific day**
  
    mnem -a 'Testing' -m -d 1 
  

The above command tells mnem to display the note in the day 1 of each month along the
current year.

**Display a note daily at a specific time**
  
    mnem -a 'Cool note.' -m  -d  -r 15 -e 30 
    
    
**Display a note on a specific date**

    
    mnem -a 'this is a note.' -y 2016 2018 -m 3 -u 10 -i 44 -d 18

It will display a note when it is 18/03/2016 at 10:44 am. and when it is
18/03/2018 at 10:44 too.

**Find notes**

    mnem -f 'somestring'

It finds all set of notes that contains 'somestring' in. You can also combine the 
letter doubled arguments -ii, -mm, -uu, -yy, -dd to perform searches in the mnem database.

Like in:

    mnem -f 'somestring' -ii 20 -dd 20

That would find all notes that contain 'somestring' and are going to be displayed at a datetime
like YY:MM:20 HH:20:SS.

