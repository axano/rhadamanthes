#!/bin/bash


function read_csv() {
	filename=$1
	res=""
#Rule 1
	if grep -i -q "<html>" "$filename"; then
		res+="y "
	else
		res+="n "
	fi
#Rule 2
	if grep -i -q "Account" "$filename"; then
        	res+="y "
	else
        	res+="n "
	fi
#Rule 3
	if grep -i -q "Dear" "$filename"; then
        	res+="y "
	else
        	res+="n "
	fi
#Rule 4
	if grep -i -q "PayPal" "$filename"; then
        	res+="y "
	else
        	res+="n "
	fi
#Rule 5
	if grep -i -q "Login" "$filename"; then
        	res+="y "
	else
        	res+="n "
	fi
#rule 6
	if grep -i -q "Bank" "$filename"; then
        	res+="y "
	else
        	res+="n "
	fi
#Rule 7
	if grep -i -q "Verify" "$filename"; then
        	res+="y "
	else
        	res+="n "
	fi
#Rule 8
	if grep -i -q "Agree" "$filename"; then
        	res+="y "
	else
       		res+="n "
	fi
#Rule 9
	if grep -i -q "Suspend" "$filename"; then
        	res+="y "
	else
        	res+="n "
	fi
#Rule 10
	if grep -E -o 'src=".*(\.png|\.jpg)' "$filename"; then
        	res+="y "
	else
        	res+="n "
	fi
#Rule 11
	emails=$(cut -f5 -d ',' $filename | grep -E -o "\b[a-zA-Z0-9.-]+@[a-zA-Z0-9.-]+.[a-zA-Z0-9.-]+\b" | grep -v "OUTLOOK")

	urls=$(cut -f4 -d ',' $filename | egrep -o 'https?://[^ ]+')

	while IFS= read -r var; do
		i=0
		reply=$(grep -o . <<<$var)
		while IFS= read -r ch; do
			[ $ch = "." ] && ((i++))
		done <<< "$reply"
		if [ "$i" -gt 2 ];then
			break
		fi
	done <<< "$emails"

	if [ "$i" -gt 2 ]; then
		res+="y "
	else
		res+="n "
	fi
#Rule 12
	if grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" <<<"$urls"; then
		res+="y "
	else
		res+="n "
	fi
#Rule 13	
	while IFS= read -r mail; do
		email=$mail
		break
	done<<< "$emails"

	match="n "
	while IFS= read -r sender; do
		email=$(tr '[:upper:]' '[:lower:]' <<<"$email")
		sender=$(tr '[:upper:]' '[:lower:]' <<<"$sender")
		if [ $email != $sender ]; then
			echo "$email $sender"
 			match="y "
			break
		fi
	done <<< "$emails"
	res+=$match
#Rule 14
	domains=$(awk -F\/ '{ a[$1"//"$3]++ } END {for (i in a) print a[i], i }' <<<"$urls")

	#std email from Ordina contains 7 URLs
	i=-7
	while IFS= read -r domain; do
		((i++))
	done<<< "$domains"

	if [ "$i" -gt 0 ]; then
		res+="y "
		echo $domains
	else
		res+="n "
	fi
#Rule 15
	#At least 5 HEXA chars required
	match="n "
	while IFS= read -r url; do
		if [[ "$url" =~ .*\/[a-fA-F0-9]{5,}\/.* ]]; then
			match="y "
			break
		fi
	done<<< "$urls"
	res+=$match

#return results
	echo $res
}

file="../Decision tree/bin/tree_data.txt"
echo "1" > "$file"
echo "15" >> "$file"
echo "Does the email body contains HTML content?
Checks if the email contains the term “Account”.
Checks if the email contains the term “Dear”.
Checks if the email contains the term “PayPal”.
Checks if the email contains the term “Login”.
Checks if the email contains the term “Bank”.
Checks if the email contains the term “Verify”.
Checks if the email contains the term “Agree”.
Checks if the email contains the term “Suspend”.
Are there more than two dots that exist in a URL in the email?
Is there an image URL?
Is there an URL whose domain is specified as an IP address?
Is there an URL whose label is different from its anchor in the email?
Is there a domain in the URLs that exists in the email?
Is there an URL consisting of hexadecimal characters in the email?
">> "$file"

i=0
while IFS=; read -r sender date subject body header urls; do
	answers=$(read_csv $body 2> /dev/null)
	answers="email$i "$answers
	echo $answers >> "$file"
	((i++))
done < ../$1
