# CMPE 230 Compiler Project

This was an assignment given to us as a part of our CMPE 230 course in Boğaziçi University Computer Engineering Undergraduate Program on Spring 2018 term.
[Specifications of the assignment is included in the repository.](/cmpe230spring2018hw2.pdf)
[The report we submitted with the assignment is included as well.](/CMPE230FILELIST-Documentation.pdf)
Our goal was to create a simple file listing utility for linux terminal in pyhton.

## Implementation

Implementation is explained in the code with comments in detail. In short our program follows these steps:

* Detect the options and their parameters from the given arguments.
* Keep the needed info in variables.
* Put rest of the arguments in a list since these are the directories.
* Acquire the files in this directories and put them in a list.
* Apply the options.

Possible options are explained in the [assignment PDF.](/cmpe230spring2018hw2.pdf)

### How to run

Download the ‘filelist.py’ file. Use these commands in the console after replacing the location of the
file.

```
chmod +x filelist.py
export PATH=$PATH:/<INSERT THE LOCATION TO HERE>
```

## Programs used

* Notepad++

## Authors

* **Burak Çetin**
* **Burhan Akkuş**

## License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.

## Acknowledgments

* Our instructor in the course, Can Öztüran
* Our classmates