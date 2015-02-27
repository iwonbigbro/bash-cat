Bash Coverage Analysis Tool
===========================

Yet Another Bash Coverage Tool?  Yes.

Why?  Because I wanted a tool that I did not have to install, build or require
any special dependencies or pre-requisits.

History
=======

Some build environments have constraints on them that often mean you don't have
network access, you have legacy tools and are unable to update, install or build
tools required to run some scripts.  An example is Ruby.  Ruby can be installed
out of the standard distro, but is often not installed by default.  Python on
the other hand, has been installed, along with Perl, in almost all environments
I have had the displeasure of running builds in.  Additionally, Ruby and NodeJS
alike, have their own package management and repositories.  Scripts written in
either language in my own experience, have always had dependencies on some NPM
or RVM package unavailable to my build environment.  However, python is slightly
different, especially if your scripts are kept stupid simple.

So because of my obscure environments, I initially looked at 'shcov'.  This was
initially a good tool, but some of the advanced scripting methods inhibited this
tools techniques for instrumenting or tracing executed lines of Bash.  It was
nearly there and I had pushed in some upstream fixes to work around some known
issues.  However, the strategy used by shcov was slightly off, so I have decided
to start again.  This time, I will take advantage of features built into Bash
that allow a more complex approach to tracing execution and getting feedback.

Say hello to bash-cat.
