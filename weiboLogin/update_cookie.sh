new_cookie=$(python3 getCookie.py $1 $2)
sed -i -e "s/.*new_cookie.*/new_cookie = {\"Cookie\"\:\"$new_cookie\"}/g" config.py
