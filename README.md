# Flashcards

## Original Inspirations

This is a project I created for my 10th grade MYP Core Passion Project @ [WIHI](https://www.wihi.org)

I'd been doing python-y things for a decent while when I started (like a year and a half), but it was stuff with pretty
limited applications (all console scripts; not everyone's got an interpreter/the know-how to run it!) So I thought I'd
try to find a way to make my things more accessible to most, and GUIs are all the rage since like the 80s, so may as
well! After some (very little) research I settled on tkinter as my library of choice, and started reading *[Python GUI
Programming with Tkinter - Second Edition](https://www.packtpub.com/product/python-gui-programming-with-tkinter-second-edition/9781801815925)*
to learn and practice.

## Goals & Specifications

I started with some pretty specific stuff in mind, I hate all the ads, bloatiness, and paywalls of sites like quizlet
and not-made-by-me-iness of existing apps like [Anki](https://apps.ankiweb.net), so thought I may as well make a
flashcard app. I also thought it'd be relatively simple & doable with my existing knowledge, allowing me to focus on the
new GUI things.

Here's a nice li'l table I made as a part of the proposal, detailing what I want to get done:

| **Capability**                   | **Specification**                                                            | **Justification**                                                                                                                                                                                                                | **Measurement of Success**                                                                                                                                                                                                                                     |
|----------------------------------|------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *Reviews*                        | Can use existing flashcard sets to review information                        | The most basic function of flashcards (and apps thereof) isto be used as a study tool. It’s important that my application can help the user review the topics of their flashcards.                                               | Application allows for use of existing flashcard sets to review information                                                                                                                                                                                    |
| *Quizzes*                        | Can quiz users (and record & display their score) on existing flashcard sets | It’s important to be tested on the information in a more restrictive way as well, so it’s good to include a feature that can make sure that a user is ready for a test on the information in the flashcards.                     | Application has an option to ‘quiz’ which can ask for the definition of each card and keep track of correct & incorrect answers (allowing for loose capitalization, missing punctuation, etc.) then display results (alongside correct answers) to the user.   |
| *Creates*                        | Can create flashcard sets                                                    | Another important function is to create review sets based on class material. My app should be able to take user input as a flashcard set.                                                                                        | Application has an option to ‘create’ which asks for terms and definitions to create a flashcard set.                                                                                                                                                          |
| *Serializes*                     | Can save and load flashcard sets                                             | My app should also be able to remember a user’s input and save it, with the ability to load and use it later. This is necessary to make the app functional, it should be able to keep working after being opened more than once. | Application has an option to ‘save’ after creating a flashcard set which serializes the data into a csv. It also has an option to ‘load’ a set at the very beginning which displays a list of saved sets to choose from, once selected can ‘review’ or ‘quiz’. |
| *Is usable for a non-programmer* | Can be run as a desktop application without a Python interpreter             | The point of this project is to make my Python-ing more accessible, and it defeats the purpose if there’s a GUI but it still needs to be run from the command line.                                                              | Application can be run (semi-)natively using PyInstaller (or a comparable packager) instead of requiring a Python interpreter and use of the command line.                                                                                                     |

## Process & Development

This was maybe one of my bigger projects ever, started with learning some stuff from the book while starting work on the
app too. You can see a more detailed (yet terrible and irregularly updated) work
schedule [here](https://docs.google.com/document/d/1a-bONauFTKrdpeRKbu78lVkhS57aC109T8Y9lNCu5O4/edit?usp=sharing)

## Support My Programming Journey

I dunno, I have enough money from jobs & studies, and whatever else, I guess just get in touch if you have any cool
opportunities for me to try out. You can use GitHub or shoot me an
email at [ashtein120@gmail.com](mailto:ashtein120@gmail.com).

Thanks for checking this thing out!
