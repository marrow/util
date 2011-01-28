# encoding: utf-8

import re

__all__ = ['escape_slashes', 'escape_percents', 'unescape']


escapes = re.compile(r'(\\[^\\]\([^\)]+\)|\\[^\\]|\\\\|%[^%][\w]?|%%|\$\([^\)]+\)|\$\$)')

escape_slashes = dict(t="\t", n="\n", r="\r", k="\033[K", rk="\r\033[K")
escape_slashes['s(normal)']     = "\033[0m"

escape_slashes['s(bold)']       = "\033[1m"
escape_slashes['s(intense)']    = "\033[1m"
escape_slashes['s(dim)']        = "\033[2m"
escape_slashes['s(italic)']     = "\033[3m"
escape_slashes['s(underline)']  = "\033[4m"
escape_slashes['s(inverse)']    = "\033[7m"
escape_slashes['s(hidden)']     = "\033[8m"
escape_slashes['s(strike)']     = "\033[9m"

escape_slashes['c(black)']      = "\033[30m"
escape_slashes['c(red)']        = "\033[31m"
escape_slashes['c(green)']      = "\033[32m"
escape_slashes['c(yellow)']     = "\033[33m"
escape_slashes['c(blue)']       = "\033[34m"
escape_slashes['c(magenta)']    = "\033[35m"
escape_slashes['c(cyan)']       = "\033[36m"
escape_slashes['c(white)']      = "\033[37m"
escape_slashes['c(default)']    = "\033[39m"

escape_slashes['b(black)']      = "\033[40m"
escape_slashes['b(red)']        = "\033[41m"
escape_slashes['b(green)']      = "\033[42m"
escape_slashes['b(yellow)']     = "\033[43m"
escape_slashes['b(blue)']       = "\033[44m"
escape_slashes['b(magenta)']    = "\033[45m"
escape_slashes['b(cyan)']       = "\033[46m"
escape_slashes['b(white)']      = "\033[47m"
escape_slashes['b(default)']    = "\033[49m"

#escape_slash_function['c(rainbow)'] - Rotate through all 16 colors.
#escape_slash_function['c(stripe)'] - Alternate between highlight and normal.
#escape_slash_function['c(duotone'] - Alternate between two colors passed as comma-separated escapes.

escape_percents = dict(t="\t", r="\n", b=' ')

# %xN - h=highlight - n=normal - f=flashing - u=underline - i=invert - 

def unescape(caller, text, obj=None):
    gender = getattr(caller, 'gender', caller.get('gender', 'it'))[0] if caller else 'i'
    
    local_slashes = dict()
    
    local_percents = dict(
            s = dict(m="he", f="she", i="it", g="they")[gender],        # subjective: he, she, it, they
            o = dict(m="him", f="her", i="it", g="them")[gender],       # objective: him, her, it, them
            p = dict(m="his", f="her", i="its", g="their")[gender],     # posessive: his, her, its, their
            a = dict(m="his", f="hers", i="its", g="theirs")[gender],   # absolute posessive: his, hers, its, theirs
            S = dict(m="He", f="She", i="It", g="They")[gender],        # subjective: he, she, it, they
            O = dict(m="Him", f="Her", i="It", g="Them")[gender],       # objective: him, her, it, them
            P = dict(m="His", f="Her", i="Its", g="Their")[gender],     # posessive: his, her, its, their
            A = dict(m="His", f="Hers", i="Its", g="Theirs")[gender],   # absolute posessive: his, hers, its, theirs
            N = caller.name if caller else 'Anonymous',
            # l = ("#%d" % ( caller.location.id, )) if caller else '%l',
            # c = caller.properties['__last_command'] if caller and '__last_command' in caller.properties else '%c',
        )
    local_percents['#'] = ("#%d" % ( caller.id, )) if caller else '%#'
    local_percents['@'] = local_percents['#']
    
    def process(match):
        match = match.group(0)
        
        if match == '\\\\': return "\\"
        elif match == '%%': return '%'
        elif match == '$$': return '$'
        
        if match.startswith('\\') and match[1:] in escape_slashes: return escape_slashes[match[1:]]
        if match.startswith('%') and match[1:] in escape_slashes: return escape_slashes[match[1:]]
        
        if match.startswith('\\') and match[1:] in local_slashes: return local_slashes[match[1:]]
        if match.startswith('%') and match[1:] in local_percents: return local_percents[match[1:]]
        
        if match.startswith('$(') and match.endswith(')') and obj:
            match = match[2:-1].split('.')
            ref = obj
            for i in match:
                ref = getattr(ref, i, ref.get(i, None))
            return unescape(caller, str(ref), obj)
        
        return match
    
    return escapes.sub(process, text)
