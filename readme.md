# Desktop Calendar

This is a side project I worked on the weekend of 06/24/23 - 06/25/23 because I wanted to be able to see my calendar events on my desktop.

It's basically a `rainmeter skin` that displays calendar events on my desktop, with `python working` behind the scenes to fetch calendar events.

The build will look (already looks) like the screenshot below.

A few steps are left to make it a partly complete project. 

![Desktop Calendar](https://github.com/leonkoech/dsktp-calendar/assets/39020723/0ac20a1d-47de-4e8d-b35e-6a2291333d46)

# Project Completion

At the moment, it's not fully complete. But you can follow along with the following tasks 

- [x] Get the calendar API Working
- [x] Read the [rainmeter](https://docs.rainmeter.net/) documentation and create components 
- [ ] `Python` scripts to emulate the code written in `Lua` as rainmeter is compatible with `Lua`
- [ ] bash script to call the python scripts at particular times of the day, preferably 7:00 am every morning
- [ ] bash script to install rainmeter, the requirements of this project and add them to files. Basically automate everything
- [ ] ** hopefully create a website for this project since i'll probably take it to prod as opensource w/ <100 people for beta

# Requirements

I used `python 3.9.7` on this project, but it should generally work on `> python 3.8` (?)

Atm rainmeter is required [download here](https://docs.rainmeter.net/manual/installing-rainmeter/)

You'll also need a credentials.json in a .env folder (root) like below

```
├───.env
    └───credentials.json
├───components
└───(your python virtual env)
```
# Installation
Since the project is still underway at 1800 HRS EST 06/25/23, there's still some things required 
