def longestPalindrome(self, s):
    n = len(s)
    if n == 0:
        return ""
    if n == 1:
        return s
    
    minstart = 0
    maxlen = 0
    
    i = 0
    while i < n:
        if n - i < maxlen / 2:
            break
        
        l = i
        r = i
        
        # Find the center of the palindrome
        while r < n - 1 and s[r] == s[r + 1]:
            r += 1
        
        # Update the next starting point
        i = r + 1
        
        # Expand around the center to find the longest palindrome
        while l > 0 and r < n - 1 and s[l - 1] == s[r + 1]:
            l -= 1
            r += 1
        
        newlen = r - l + 1
        if newlen > maxlen:
            maxlen = newlen
            minstart = l
    
    return s[minstart:minstart + maxlen]