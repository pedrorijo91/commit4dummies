# git-scripts

Simple python script to be used as a git hook, avoiding commiting unwanted debug (and other undesired code) functions.

Default configurations looking only for few cases:

* .java files
  * print
  * TODO
* .py files
  * print
  * TODO

Example configuration file ('keywords.conf') with unrealistic examples just for demonstration purposes:

* .java files
  * exp
  * print
  * TODO
  * foo 
* .txt files
  * testing
  * xpto
  * bar
