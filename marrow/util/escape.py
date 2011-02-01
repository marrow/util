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
            s = dict(m="he",      f="she",     i="it",     o="it",     n="ze",      s="e",      g="they")[gender],       # subjective
                                                                                                                         #   second-person formal (you)
                                                                                                                         #   second-person informal (thou)
            o = dict(m="him",     f="her",     i="it",     o="it",     n="hir",     s="em",     g="them")[gender],       # objective
                                                                                                                         #   direct
                                                                                                                         #   indirect
            v = dict(m="him",     f="her",     i="it",     o="it",     n="hir",     s="em",     g="them")[gender],       # partitive
                                                                                                                         # first-person posessive adjective (my, our)
                                                                                                                         # first-person posessive pronoun (mine, ours)
            p = dict(m="his",     f="her",     i="its",    o="its",    n="hir",     s="eir",    g="their")[gender],      # third-person possessive adjective
            a = dict(m="his",     f="hers",    i="its",    o="its",    n="hirs",    s="eirs",   g="theirs")[gender],     # third-person possessive pronoun
            f = dict(m="himself", f="herself", i="itself", o="itself", n="hirself", s="emself", g="themselves")[gender], # reflexive
                                                                                                                         # inclusive we
                                                                                                                         # exclusive we
                                                                                                                         # reciprocal (each other)
                                                                                                                         # prepositional (X and Y looked at _him_)
                                                                                                                         # disjunctive (me)
                                                                                                                         # demonstrative (this)
                                                                                                                         # indefinite (some)
                                                                                                                         # interrogative (who, which)
            
            S = dict(m="He",      f="She",     i="It",     o="It",     n="Ze",      s="E",      g="They")[gender],       # subjective
            O = dict(m="Him",     f="Her",     i="It",     o="It",     n="Hir",     s="Em",     g="Them")[gender],       # objective
            V = dict(m="Him",     f="Her",     i="It",     o="It",     n="Hir",     s="Em",     g="Them")[gender],       # partitive
            P = dict(m="His",     f="Her",     i="Its",    o="Its",    n="Hir",     s="Eir",    g="Their")[gender],      # possessive adjective
            A = dict(m="His",     f="Hers",    i="Its",    o="Its",    n="hirs",    s="Eirs",   g="Theirs")[gender],     # possessive pronoun
            F = dict(m="Himself", f="Herself", i="Itself", o="Itself", n="Hirself", s="Emself", g="Themselves")[gender], # reflexive
            
            N = getattr(caller, 'name', caller.get('name', 'Anonymous')) if caller else 'Anonymous',
            # l = ("#%d" % ( caller.location.id, )) if caller else '%l',
            # c = caller.properties['__last_command'] if caller and '__last_command' in caller.properties else '%c',
        )
    
    local_percents['#'] = ("#%s" % ( getattr(caller, 'id', caller.get('id', '%#')), )) if caller else '%#'
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
