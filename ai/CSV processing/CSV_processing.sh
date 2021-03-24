#!/bin/bash


function read_csv() {
	filename=$1
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

	if grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" <<<"$urls"; then
		res+="y "
	else
		res+="n "
	fi

	email=(${emails[@]})
	match="n "
	while IFS= read -r sender; do
		email=$(tr '[:upper:]' '[:lower:]' <<<"$email")
		sender=$(tr '[:upper:]' '[:lower:]' <<<"$sender")
		if [ "$email" != "$sender" ]; then
 			match="y "
			break
		fi
	done <<< "$emails"
	res+=$match

	domains=$(awk -F\/ '{ a[$1"//"$3]++ } END {for (i in a) print a[i], i }' <<<"$urls")

	#std email from Ordina contains 5 URLs
	i=-5
	while IFS= read -r domain; do
		((i++))
	done<<< "$domains"

	if [ "$i" -gt 0 ]; then
		res+="y "
		echo $domains
	else
		res+="n "
	fi

	#At least 5 HEXA chars required
	match="n "
	while IFS= read -r url; do
		if [[ "$url" =~ .*\/[a-fA-F0-9]{5,}\/.* ]]; then
			match="y "
			echo $url
			break
		fi
	done<<< "$urls"
	res+=$match

	echo $res
}
while IFS=, read -r sender date subject body header urls; do
	read_csv $body 2> /dev/null
done < ../$1
