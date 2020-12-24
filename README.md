### Hi there 👋
# SG Smart Mirror

Python Powered:
[![N|Solid](https://raw.githubusercontent.com/willtheorangeguy/Python-Logo-Widgets/master/pythonpoweredlengthgif.gif)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)


SG Smart Mirror is a python-based smart mirror built for Singaporeans. It's module-based design makes it easy for users to customize widgets to show on the user interface. This is just the prototype, similar to the web-based [MagicMirror²](https://github.com/MichMich/MagicMirror), you can customized the modules however you like (although we do not have a community to help with the contributions). 

The reason for starting this project is due to the lack of use-cases for Singaporean users in the  [MagicMirror²](https://github.com/MichMich/MagicMirror) community. Also, I can't contribute to the MagicMirror² community because I have no experience in web development xD, the libraries and frameworks out there is just too confusing for me.

### Preview
[![SmartMirror Preview](https://j.gifs.com/gZwQQj.gif)](https://j.gifs.com/gZwQQj.gif)

### Current Features

  - Date/Time widget
  - Weather widget showing temperature readings from multiple locations in Singapore
  - Webapp widget (Instagram, YouTube, Reddit, CNA)
  - Traffic widget (currently only for busses)
  - News widget with keyword highlighting (e.g. Highlight headline that contains the word 'arrested')

You can also:
  - Customize the locations of the weather widgets
  - Drag the modules around the user interface

### Future Features
- Show regions that are raining in real-time
- Music player (?) OR YouTube bookmark function + add new app icon to Webapp widget
- Speech recognition (?) / Voice activation
- Gesture recognition (?) [Still deciding between Leap or Camera]
- Display on-screen keyboard for web app usage

### Cons
- The size of widgets are fixed, didn't had rescaling in mind when I first designed the system.

### Deployment
Deployment can be done on Raspberry Pi or any Windows platform. It is best if you integrate an IR frame so that your mirror is 'touchscreen'. 

