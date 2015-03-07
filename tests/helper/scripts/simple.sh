#!/bin/bash

# A simple script with no recursion.

function a_function() {
    echo "return text"
}

a_function_ret=$(a_function)

cat <<-SIMPLE_HEREDOC
A simple here doc.
SIMPLE_HEREDOC

cat <<<"An inline here doc"

echo A multiline \
    statement
