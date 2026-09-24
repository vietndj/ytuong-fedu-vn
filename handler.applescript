on open location this_URL
    do shell script "python3 /Users/vietmac/Documents/CODE/ytuong-fedu-vn/url_handler.py '" & this_URL & "' > /dev/null 2>&1 &"
end open location
