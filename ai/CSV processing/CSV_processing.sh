#!/bin/bash

filename="../dump.csv"
res=""
if grep -i -q "<html>" "$filename"; then
	res+="y "
else
	res+="n "
fi

if grep -i -q "Account" "$filename"; then
        res+="y "
else
        res+="n "
fi

if grep -i -q "Dear" "$filename"; then
        res+="y "
else
        res+="n "
fi

if grep -i -q "PayPal" "$filename"; then
        res+="y "
else
        res+="n "
fi

if grep -i -q "Login" "$filename"; then
        res+="y "
else
        res+="n "
fi

if grep -i -q "Bank" "$filename"; then
        res+="y "
else
        res+="n "
fi

if grep -i -q "Verify" "$filename"; then
        res+="y "
else
        res+="n "
fi

if grep -i -q "Agree" "$filename"; then
        res+="y "
else
        res+="n "
fi

if grep -i -q "Suspend" "$filename"; then
        res+="y "
else
        res+="n "
fi


if grep -E -o 'src=".*(\.png|\.jpg)' "$filename"; then
        res+="y "
else
        res+="n "
fi

emails=$(cut -f5 -d ',' $filename | grep -E -o "\b[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+.[a-zA-Z0-9.-]+\b" | grep -v "OUTLOOK")

urls=$(cut -f4 -d ',' $filename | egrep -o 'https?://[^ ]+')

echo $emails
echo $urls


echo $res
